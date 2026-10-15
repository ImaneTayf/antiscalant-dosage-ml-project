import matplotlib.pyplot as plt

def plot_results(metrics, predictions):
    fig, axes = plt.subplots(1, 3, figsize=(16, 4), constrained_layout=True)
    metrics[["MAE", "RMSE"]].plot.bar(ax=axes[0], rot=35)
    axes[0].set_ylabel("Synthetic dose index error")
    axes[0].set_title("Synthetic holdout errors")
    axes[1].plot(predictions.timestamp, predictions.actual, label="Synthetic observed", alpha=.7)
    axes[1].plot(predictions.timestamp, predictions.Ridge, label="Ridge")
    axes[1].set_title("Chronological holdout (Ridge example)")
    axes[1].set_ylabel("Synthetic dose index")
    axes[1].tick_params(axis="x", rotation=35)
    axes[1].legend()
    axes[2].scatter(predictions.Ridge, predictions.actual-predictions.Ridge, s=10, alpha=.5)
    axes[2].axhline(0, color="black", linewidth=1)
    axes[2].set(xlabel="Ridge prediction", ylabel="Observed minus predicted",
                title="Synthetic residuals")
    return fig
