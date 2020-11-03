import argparse
import itertools

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("darkgrid")
sns.set(font_scale=1.2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results_dir", type=str)
    config = parser.parse_args()

    results = pd.read_csv(config.results_dir + "/results.csv")

    for steps, init_cars in itertools.product([500, 1000, 1500], [500, 750, 1000]):
        selection_results = results[
            (results["max_steps"] == steps) & (results["init_cars"] == init_cars)
        ]
        ax = sns.boxplot(
            x="sim_type", y="av_travel_time", data=selection_results, palette="Greens_d"
        )
        ax.set(ylabel="Average Travel Time (s)", xlabel="")
        plt.savefig(config.results_dir + f"/boxplot_travel_{steps}_{init_cars}.png")
        plt.cla()

        ax = sns.boxplot(
            x="sim_type",
            y="av_waiting_agents",
            data=selection_results,
            palette="Greens_d",
        )
        ax.set(ylabel="Average % waiting vehicles", xlabel="")
        plt.savefig(config.results_dir + f"/boxplot_waiting_{steps}_{init_cars}.png")
        plt.cla()

        ax = sns.boxplot(
            x="sim_type",
            y="travel_time_index",
            data=selection_results,
            palette="Greens_d",
        )
        ax.set(ylabel="Travel time index", xlabel="")
        plt.savefig(config.results_dir + f"/boxplot_tti_{steps}_{init_cars}.png")
        plt.cla()
