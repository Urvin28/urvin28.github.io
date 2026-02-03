import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb

# =========================
# 1. Load Data
# =========================

df = pd.read_csv(r"creditcard.csv")
X = df.drop(columns=['Class'])
y = df['Class']

# =========================
# 2. Split Data
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

x_train_sub, x_val, y_train_sub, y_val = train_test_split(X_train  , y_train,
                                                          test_size=0.2, stratify= y_train, random_state=42)


dtrain = xgb.DMatrix(x_train_sub, label = y_train_sub)
dval = xgb.DMatrix(x_val, label = y_val)
dtest = xgb.DMatrix(X_test, label = y_test)


parameters = {
    'objective' : 'binary:logistic',
    'max_depth': 6,
    'learning_rate': 0.05,
    'scale_pos_weight': (y_train ==0).sum() / (y_train ==1).sum(),
    'eval_metric': 'auc'
}

evals = [(dtrain, 'train'), (dval, 'val')]

model = xgb.train(
    parameters,
    dtrain,
    num_boost_round=2000,
    evals=evals,
    early_stopping_rounds=100,
    verbose_eval =20
)

y_prob = model.predict(dtest)

threshold = 0.2
y_pred = (y_prob >= threshold).astype(int)

print(classification_report(y_test, y_pred))

print('ROC_AUC:', roc_auc_score(y_test, y_prob))

import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score

# Probabilities from XGBoost
y_prob = model.predict(dtest)

# Thresholds to evaluate
thresholds = np.linspace(0, 1, 100)

precision_list = []
recall_list = []

for t in thresholds:
    y_pred_t = (y_prob >= t).astype(int)
    precision_list.append(precision_score(y_test, y_pred_t, zero_division=0))
    recall_list.append(recall_score(y_test, y_pred_t))

# Plot Precision and Recall vs Threshold
plt.figure(figsize=(10,6))
plt.plot(thresholds, recall_list, label='Recall', color='red', linewidth=2)
plt.plot(thresholds, precision_list, label='Precision', color='blue', linewidth=2)
plt.axvline(x=0.2, color='green', linestyle='--', label='Chosen Threshold (0.2)')
plt.title('Precision & Recall vs Threshold for Fraud Detection')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.legend()
plt.grid(True)
# save plot to file
plt.tight_layout()
plt.savefig('precision_recall.png', dpi=150)
print('Saved precision_recall.png')

# save model artifact
import joblib
try:
    joblib.dump(model, 'credit_xgb.joblib')
    print('Saved model to credit_xgb.joblib')
except Exception:
    pass
