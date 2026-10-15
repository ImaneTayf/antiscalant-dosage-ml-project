# Antiscalant Dosage — Data & Machine Learning Portfolio

> This repository presents a sanitized demonstration of a Data & Machine Learning project conducted during an industrial internship. Original industrial data cannot be shared for confidentiality reasons; the included dataset is synthetic.

## Project context and actual scope

The internship concerned analysis and prediction of historical antiscalant dosage in industrial desalination. The work covered preparation and temporal alignment of process-control and laboratory data, data quality checks, feature engineering, and comparison of Ridge, Partial Least Squares (PLS), Huber and Random Forest regression against a median baseline.

This public implementation was written separately for a Data Science internship application. It demonstrates those methodological steps with invented signals. It is not the original internship code, dataset or a reproduction of industrial results. No industrial performance numbers, operating limits, internal filenames or site-specific details are included.

## What the demonstration does

1. Generates hourly synthetic process signals and less frequent synthetic laboratory observations using a fixed random seed.
2. Removes duplicate timestamps and masks deliberately injected invalid values; preserves missing predictors for training-only imputation.
3. Aligns each process timestamp with the latest available laboratory observation, with an illustrative 18-hour expiration. There is no future laboratory lookup or backward filling.
4. Adds a past-only rolling flow mean and a salinity–flow interaction.
5. Uses the earliest 80% of observations for training and the latest 20% for evaluation, without shuffling. Imputation and scaling are fitted only on training data.
6. Compares five fixed model configurations using MAE, RMSE and R²; exports comparison, timeline and residual plots.

These particular synthetic features, settings and split proportions are demonstration choices, not claims about the exact internship implementation. The holdout is a single demonstration evaluation; there is no hyperparameter search or model selection based on it.

## Reproduce

Python 3.9–3.12 is recommended for these pinned dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m src.run_demo
python -m unittest discover -s tests
jupyter lab notebooks/01_synthetic_demo.ipynb
```

Select the environment's Python kernel, then **Restart Kernel and Run All Cells**. The notebook generates its data from scratch; no private files or credentials are needed. Run the command-line demonstration to regenerate the included synthetic CSVs and report artifacts.

## Repository structure

```text
 data/synthetic/                 Generated fictional process and laboratory CSVs
 notebooks/01_synthetic_demo.ipynb  Executed, reproducible walkthrough
 src/synthetic.py               Seeded synthetic data generation
 src/preprocessing.py           Quality checks and availability-time alignment
 src/features.py                Causal feature engineering
 src/modeling.py                Train-only preprocessing and five regressors
 src/plots.py                   Evaluation visualizations
 src/run_demo.py                End-to-end entry point
 reports/                       Synthetic metrics, predictions and plot
 tests/                         Leakage and baseline checks
 requirements.txt               Pinned direct dependencies
```

## Synthetic data dictionary

All numerical signals are **dimensionless invented indices**, not physical concentrations, plant measurements or recommended doses. Timestamps are fictional UTC dates.

| Column | Meaning in this demonstration |
|---|---|
| `timestamp` | Hourly prediction timestamp |
| `flow_index` | Fictional process flow signal |
| `temperature_index` | Fictional process temperature signal |
| `dose_index` | Fictional regression target |
| `available_at` | Time a synthetic laboratory result becomes available |
| `salinity_index` | Fictional laboratory signal |
| `lab_age_hours` | Age of the most recently available result |
| `flow_previous_6h` | Mean over the previous six hourly rows, excluding the current row |
| `salinity_flow_interaction` | Product of two synthetic predictors |

The generator uses a deliberately simple equation plus random noise. It does not simulate desalination chemistry, membrane scaling, laboratory delays or real operating policies. The rolling window assumes the generator's regular hourly grid. Real data would require additional timestamp and sampling checks.

## Results and interpretation

[Computed metrics](reports/synthetic_metrics.csv) and [holdout predictions](reports/synthetic_predictions.csv) are produced exclusively from the synthetic dataset. MAE and RMSE are in synthetic dose-index units; R² is dimensionless. Lower MAE/RMSE and higher R² are preferable on this holdout. The baseline predicts the **training target median** for every held-out observation.

![Synthetic evaluation only](reports/synthetic_evaluation.png)

These scores illustrate pipeline execution only. They do not establish industrial accuracy, savings, deployment readiness or superiority of a model on the confidential project. Ridge is shown in the time-series and residual examples by design, not because it was selected as the best industrial model.

Predicting an observed dosage does not establish the chemically optimal dose. This repository is not an operational dosing tool. No production deployment, causal benefit, economic gain or real-world validation is claimed.

## Confidentiality

Only newly generated synthetic data and newly written demonstration code belong here. Do not add original exports, reports, screenshots, trained industrial models, internal identifiers or their derived statistics. The synthetic distribution and generator parameters were not fitted to confidential observations. `.gitignore` is a convenience, not a confidentiality guarantee: review staged contents and Git history before any public push.
