import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation_heatmap(corr,filename):

    plt.figure(figsize=(10,8))

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        center=0
    )

    plt.title(filename)

    plt.tight_layout()

    plt.savefig(
        f"reports/plots/{filename}.png"
    )

    plt.close()
    


def plot_rolling_correlation(roll_corr):

    plt.figure(figsize=(12,6))

    for column in roll_corr.columns:
        plt.plot(
            roll_corr.index,
            roll_corr[column],
            label=column
        )
        
    #plt.plot(roll_corr.index,roll_corr['copper_20d'],label='copper_20d')

    plt.title("252-Day Rolling Correlation with OMX Returns")

    plt.xlabel("Date")
    plt.ylabel("Correlation")

    plt.legend(
        bbox_to_anchor=(1.05,1),
        loc="upper left"
    )

    plt.tight_layout()

    plt.savefig(
        "reports/plots/rolling_correlation.png"
    )

    plt.close()    