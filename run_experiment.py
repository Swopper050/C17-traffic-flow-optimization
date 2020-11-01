import datetime as dt
import itertools
import os
from types import SimpleNamespace

import pandas as pd

from run_dynamic_routing_simulation import run_dynamic_routing_simulation
from run_static_routing_simulation import run_static_routing_simulation

if __name__ == "__main__":

    dir_name = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(f"results/exp_{dir_name}")
    save_dir = f"results/exp_{dir_name}/results.csv"

    exp_steps = [500, 1000, 1500]
    exp_init_cars = [500, 750, 1000]

    results = pd.DataFrame(
        columns=[
            "run",
            "max_steps",
            "init_cars",
            "av_travel_time",
            "free_flow_travel_time",
            "av_waiting_agents",
            "travel_time_index",
            "sim_type",
        ]
    )
    results.to_csv(save_dir, index=False)

    for n_steps, init_cars in itertools.product(exp_steps, exp_init_cars):
        config = SimpleNamespace(
            dir="low_manhattan",
            max_steps=n_steps,
            cars_per_step=1,
            init_cars=init_cars,
        )

        for i in range(50):
            results = pd.read_csv(save_dir)

            static_results = run_static_routing_simulation(config, seed=i)
            results = results.append(
                {
                    "run": i,
                    "max_steps": config.max_steps,
                    "init_cars": config.init_cars,
                    "av_travel_time": static_results.av_travel_time,
                    "free_flow_travel_time": static_results.free_flow_travel_time,
                    "av_waiting_agents": static_results.av_waiting_agents,
                    "travel_time_index": static_results.travel_time_index,
                    "sim_type": "static",
                },
                ignore_index=True,
            )

            dynamic_results = run_dynamic_routing_simulation(config, seed=i)
            results = results.append(
                {
                    "run": i,
                    "max_steps": config.max_steps,
                    "init_cars": config.init_cars,
                    "av_travel_time": dynamic_results.av_travel_time,
                    "free_flow_travel_time": dynamic_results.free_flow_travel_time,
                    "av_waiting_agents": dynamic_results.av_waiting_agents,
                    "travel_time_index": dynamic_results.travel_time_index,
                    "sim_type": "dynamic",
                },
                ignore_index=True,
            )

            results.to_csv(save_dir, index=False)
