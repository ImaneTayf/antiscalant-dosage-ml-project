"""Run from repository root: python -m src.run_demo."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
from .synthetic import generate
from .preprocessing import prepare
from .features import engineer
from .modeling import evaluate
from .plots import plot_results

def main():
    root = Path(__file__).resolve().parents[1]
    data, reports = root/"data/synthetic", root/"reports"
    data.mkdir(parents=True, exist_ok=True)
    reports.mkdir(exist_ok=True)
    process, lab = generate()
    process.to_csv(data/"synthetic_process.csv", index=False)
    lab.to_csv(data/"synthetic_lab.csv", index=False)
    aligned, audit = prepare(process, lab)
    metrics, predictions, _, cut = evaluate(engineer(aligned))
    metrics.to_csv(reports/"synthetic_metrics.csv")
    predictions.to_csv(reports/"synthetic_predictions.csv", index=False)
    plot_results(metrics, predictions).savefig(reports/"synthetic_evaluation.png", dpi=140)
    print("SYNTHETIC DEMONSTRATION ONLY", audit, "training rows:", cut)
    print(metrics.round(4).to_string())

if __name__ == "__main__":
    main()
