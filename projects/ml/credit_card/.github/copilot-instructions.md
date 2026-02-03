<!-- Copilot instructions for AI coding agents working on this repo -->
# Copilot Instructions — credit_card project

This file gives focused, actionable guidance for AI coding assistants working on this small ML project.

- **Project purpose:** single-file ML demo training an XGBoost binary classifier on `creditcard.csv` and saving artifacts (`credit_xgb.joblib`, `precision_recall.png`). See `README.md` for quick run notes.

- **Key files:**
  - `credit.py` — main script: data load, train/val/test split, XGBoost training (`xgb.train`), plotting, and saving a `joblib` model.
  - `creditcard.csv` — required dataset (place in repo root alongside `credit.py`).
  - `credit_xgb.joblib` — saved model artifact (output). Update code only if intentionally changing artifact format.
  - `README.md` — run instructions and example results.

- **Big-picture architecture / data flow:**
  1. `credit.py` reads `creditcard.csv` into a pandas DataFrame.
  2. Features/labels split: `X = df.drop(columns=['Class'])`, `y = df['Class']`.
  3. Train/val/test split uses `train_test_split(..., stratify=..., random_state=42)`.
  4. XGBoost uses DMatrix (`xgb.DMatrix`) and `xgb.train` with `early_stopping_rounds` and `eval_metric='auc'`.
  5. Predictions saved as probabilities; a fixed threshold (`threshold = 0.2`) is used in the example to produce classification metrics and the PR plot.

- **Project-specific conventions / patterns:**
  - Uses `xgb.DMatrix` + `xgb.train` (not scikit-learn API). Adjustments to training params must respect DMatrix usage.
  - Class imbalance handled via `scale_pos_weight` computed as `(y_train ==0).sum() / (y_train ==1).sum()` — preserve this approach when changing sampling or class weighting logic.
  - Random seed is `42` across `train_test_split` calls — keep for reproducible results unless intentionally experimenting.
  - Plotting writes `precision_recall.png`; the script saves files rather than requiring an interactive display.
  - The script attempts to `joblib.dump(model, 'credit_xgb.joblib')` inside a `try/except` — expect silent failures if saving is not possible.

- **Developer workflows / commands:**
  - Create venv and install (from README):
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r ../../requirements.txt
    ```
    Note: `requirements.txt` is referenced two levels up by the README; if missing, create one with `pandas,xgboost,scikit-learn,matplotlib,joblib`.
  - Run training locally:
    ```powershell
    python credit.py
    ```
  - Quick iteration/testing: to reduce runtime for experiments, temporarily set `num_boost_round=10` and/or lower `early_stopping_rounds` in `credit.py`.

- **When editing `credit.py`: specific advice**
  - If changing model hyperparameters, update `parameters` dict near the top of the training block.
  - If switching to the scikit-learn API (`xgboost.XGBClassifier`), convert DMatrix/`xgb.train` usage consistently and update `joblib.dump` compatibility.
  - Keep `threshold = 0.2` explicit in the file or update README when changing the example threshold for plots/metrics.

- **Testing / debugging tips**
  - Reproduceable debugging: run the script with a small sample of the CSV (e.g., `df.sample(1000, random_state=42)`) to iterate faster.
  - If plots fail on headless CI, replace `plt.show()` with `plt.savefig(...)` (the script already saves `precision_recall.png`).
  - If `joblib.dump` silently fails (caught by broad `except`), remove the `try/except` locally to surface errors.

- **Integration / external dependencies:**
  - Core dependencies: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `matplotlib`, `joblib`.
  - Data: expects a local `creditcard.csv` containing `Class` label column.

- **Edit and commit guidance for AI agents:**
  - Keep changes minimal and focused to the single file being modified unless you intentionally coordinate changes (e.g., updating README when changing a default threshold).
  - When adding dependencies, update a `requirements.txt` in repo root or note the change in `README.md`.

If anything above is ambiguous or you want more examples (e.g., converting to scikit-learn API, adding a test harness, or building a minimal `requirements.txt`), ask and I'll iterate.
