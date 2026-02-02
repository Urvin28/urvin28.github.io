import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

# load dataset

df = pd.read_csv(r"Exam_Score_Prediction.csv")

x = df.drop(['exam_score', 'student_id'], axis=1)
y = df['exam_score']

# split dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# discover categorical columns from predictors only (robust to pandas string/object)
import pandas as _pd
cat_cols = [col for col in x.columns if not _pd.api.types.is_numeric_dtype(x[col])]

if len(cat_cols) > 0:
    # fit encoder on training data only to avoid data leakage
    # use dense output for easy DataFrame construction and ignore unknown categories in test
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    x_train_cat_arr = encoder.fit_transform(x_train[cat_cols])
    x_test_cat_arr = encoder.transform(x_test[cat_cols])

    # convert to dataframes with matching indices
    x_train_cat = pd.DataFrame(
        x_train_cat_arr,
        columns=encoder.get_feature_names_out(cat_cols),
        index=x_train.index
    )

    x_test_cat = pd.DataFrame(
        x_test_cat_arr,
        columns=encoder.get_feature_names_out(cat_cols),
        index=x_test.index
    )

    # drop original categorical columns and concat encoded columns
    x_train = x_train.drop(columns=cat_cols)
    x_test = x_test.drop(columns=cat_cols)

    x_train = pd.concat([x_train, x_train_cat], axis=1)
    x_test = pd.concat([x_test, x_test_cat], axis=1)
else:
    print('No categorical columns detected; skipping one-hot encoding.')

from xgboost import XGBRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib

# Randomized search over common XGBoost hyperparameters (no early stopping required)
param_dist = {
    'n_estimators': [100, 200, 300, 500, 800],
    'learning_rate': [0.01, 0.03, 0.05, 0.1],
    'max_depth': [3, 5, 6, 8],
    'subsample': [0.6, 0.8, 1.0],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'reg_lambda': [0.5, 1, 3],
    'min_child_weight': [1, 3, 5]
}

base = XGBRegressor(random_state=42, n_jobs=-1)
rnd = RandomizedSearchCV(base, param_distributions=param_dist,
                         n_iter=30, scoring='neg_root_mean_squared_error',
                         cv=5, verbose=1, n_jobs=-1, random_state=42)

print('Running RandomizedSearchCV (this may take several minutes)...')
rnd.fit(x_train.fillna(-999), y_train)

print('Best params:', rnd.best_params_)
best = rnd.best_estimator_
print('Best params:', rnd.best_params_)
best = rnd.best_estimator_

# --- K-Fold ensembling with best params to improve stability ---
from sklearn.model_selection import KFold
from copy import deepcopy

best_params = rnd.best_params_.copy()
# ensure deterministic but allow KFold randomness
cv = KFold(n_splits=5, shuffle=True, random_state=42)
models = []
test_preds = np.zeros((len(x_test), cv.get_n_splits()))
fi_sum = np.zeros(x_train.shape[1])

X_test_filled = x_test.fillna(-999)
X_train_filled = x_train.fillna(-999)

for i, (tr_idx, val_idx) in enumerate(cv.split(X_train_filled)):
    X_tr, y_tr = X_train_filled.iloc[tr_idx], y_train.iloc[tr_idx]
    X_val, y_val = X_train_filled.iloc[val_idx], y_train.iloc[val_idx]

    m = XGBRegressor(**best_params, random_state=42 + i, n_jobs=-1)
    m.fit(X_tr, y_tr, verbose=False)
    models.append(deepcopy(m))

    # accumulate test predictions for averaging
    test_preds[:, i] = m.predict(X_test_filled)

    # accumulate feature importances
    try:
        fi = m.feature_importances_
        if fi.shape[0] == fi_sum.shape[0]:
            fi_sum += fi
    except Exception:
        pass

# average predictions across ensemble
preds_avg = test_preds.mean(axis=1)
mae = mean_absolute_error(y_test, preds_avg)
r2 = r2_score(y_test, preds_avg)

print(f'Ensemble Test MAE: {mae:.4f}')
print(f'Ensemble Test R2: {r2:.4f}')

# average feature importance (if available)
try:
    fi_avg = fi_sum / cv.get_n_splits()
    import pandas as pd
    fi_series = pd.Series(fi_avg, index=x_train.columns).sort_values(ascending=False)
    print('\nTop 15 feature importances:')
    print(fi_series.head(15))
except Exception:
    pass

# save ensemble
joblib.dump(models, 'xgb_randomsearch_ensemble.joblib')
print('Saved ensemble models to xgb_randomsearch_ensemble.joblib')

# save top feature importances and a small plot if available
try:
    fi_series.head(15).to_csv('feature_importance.csv')
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,4))
    fi_series.head(15).plot(kind='bar', color=['#6c63ff','#c44d7a']*8)
    plt.title('Top 15 Feature Importances')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=150)
    print('Saved feature_importance.png')
except Exception:
    pass
