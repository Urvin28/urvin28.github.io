import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report, roc_auc_score, recall_score, precision_score
import xgboost as xgb



df = pd.read_csv(r"diabetes_dataset.csv")

leak_cols = [
    'diabetes_risk_score',
    'hba1c',
    'insulin_level',
    'diabetes_stage',
    'diagnosed_diabetes',
    'glucose_fasting',
    'glucose_postprandial'

]

x = df.drop(columns=leak_cols)
y = df['diagnosed_diabetes']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2, stratify=y, random_state=42)

# looking for categorical columns (robust: any non-numeric dtype)
import pandas as _pd
cat_cols = [c for c in x_train.columns if not _pd.api.types.is_numeric_dtype(x_train[c])]

if len(cat_cols) > 0:
    # initilizing encoder
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False, drop=None)

    # encoding cat cols
    x_train_cat_cols = encoder.fit_transform(x_train[cat_cols])
    x_test_cat_cols = encoder.transform(x_test[cat_cols])

    # converting them back to DataFrames
    x_train_cat_cols = pd.DataFrame(
        x_train_cat_cols,
        columns=encoder.get_feature_names_out(cat_cols),
        index=x_train.index
    )

    x_test_cat_cols = pd.DataFrame(
        x_test_cat_cols,
        columns=encoder.get_feature_names_out(cat_cols),
        index=x_test.index
    )

    # drop original categorical columns and concat encoded columns
    x_train = x_train.drop(columns=cat_cols)
    x_test = x_test.drop(columns=cat_cols)

    x_train = pd.concat([x_train, x_train_cat_cols], axis=1)
    x_test = pd.concat([x_test, x_test_cat_cols], axis=1)
else:
    print('No categorical columns detected; skipping one-hot encoding.')

#model
model = xgb.XGBClassifier(
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum(),
    n_estimators = 500,
    max_depth = 5,
    learning_rate =0.03,
    subsample = 0.8,
    colsample_bytree = 0.8,
    eval_metric = 'auc',
    use_label_encoder = False, 
    random_state =42

)

#fit the model
model.fit(x_train, y_train,
          eval_set = [(x_test, y_test)],

          verbose = 10
          )


#evaluation
y_prob = model.predict_proba(x_test)[:,1]

#looking for best recall
threshold = np.linspace(0.05, 0.95, 100)

best_recall = 0
best_t = 0
best_precision = 0

for t in threshold:
    y_pred_t = (y_prob >= t).astype(int)
    recall = recall_score(y_test, y_pred_t, pos_label=1)
    precision = precision_score(y_test, y_pred_t, pos_label=1)

    if recall > 0.90 and precision > best_precision:
        best_precision = precision
        best_recall = recall
        best_t = t

#print 
print(f"best threshold for recall: {best_t:.2f}")
print(f"best recall: {best_recall:.2f}")
print(f"best precision: {best_precision:.2f}")

y_pred = (y_prob >= best_t).astype(int)

print(classification_report(y_test, y_pred))

print("ROC_AUC :", roc_auc_score(y_test, y_prob))
# save model and ROC curve
import joblib
try:
    joblib.dump(model, 'diabetes_xgb.joblib')
    print('Saved model to diabetes_xgb.joblib')
except Exception:
    pass

try:
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(6,6))
    plt.plot(fpr, tpr, color='#6c63ff', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0,1],[0,1], color='grey', lw=1, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('roc_curve.png', dpi=150)
    print('Saved roc_curve.png')
except Exception:
    pass
