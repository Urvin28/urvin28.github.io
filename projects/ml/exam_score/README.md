Exam Score Prediction — notes

Place the dataset CSV `Exam_Score_Prediction.csv` in this folder.

Install dependencies (recommended in a venv):

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r ../../requirements.txt
```

Run:

```bash
python exam_score.py
```

Outputs:
- Trained ensemble saved as `xgb_randomsearch_ensemble.joblib` in this folder.

Results (this run)

- Model: XGBoost Regressor (RandomizedSearchCV then 5-fold K-Fold ensembling)
- Preprocessing: fill missing with -999, OneHot encode categorical predictors when present
- Metrics (this run): Ensemble Test MAE: 7.0958, Ensemble Test R2: 0.7341
- Top features (this run): `study_hours`, `sleep_quality_poor`, `class_attendance`, `course_b.com`, `sleep_quality_good`

Artifacts saved in this folder:
- `xgb_randomsearch_ensemble.joblib` — saved ensemble models
- `feature_importance.csv` — top feature importances
- `feature_importance.png` — bar chart of top importances

Notes: run `python exam_score.py` to reproduce these artifacts on your environment.
