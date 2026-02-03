Credit Card Fraud Detection — notes

Place the dataset CSV `creditcard.csv` in this folder.

Install dependencies (recommended in a venv):

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r ../../requirements.txt
```

Run:

```bash
python credit.py
```

Notes:
- The script expects a `creditcard.csv` with a `Class` column (0/1 labels).
- The script opens a matplotlib plot; run in an environment that supports plotting or save figures in the script.

Results (this run)

- Model: XGBoost (trained via `xgb.train` with early stopping; AUC used for eval)
- Preprocessing: train/val/test split; `scale_pos_weight` set from class imbalance
- Metrics (this run): ROC_AUC: 0.9712330099456777
- Test set classification (this run): class 1 — precision 0.73, recall 0.85, f1 0.79
- Chosen threshold in script: 0.20 (used for example PR visualization)

Visuals (example):

![Precision vs Recall across thresholds](pr_curve.svg)

Notes: the plot shows precision and recall vs threshold and a vertical line at the chosen threshold. For exact numbers run `python credit.py` after placing the dataset in this folder.
 
Artifacts saved in this folder:
- `precision_recall.png` — precision & recall vs threshold plot
- `credit_xgb.joblib` — trained model artifact
