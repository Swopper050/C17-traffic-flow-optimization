import argparse
from types import SimpleNamespace

import cityflow
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from generate_random_cars_flow_file import generate_random_flow_file
from utils import create_road_length_dict

sns.set_theme()


def run_static_routing_simulation(config, seed=69, verbose=False):
    """Runs a simulation using simple static routing.

    :param config: namespace with the configuration for the run
    :param seed: seed to use for the random cars
    :param verbose: whether or not to show user output
    """

    generate_random_flow_file(
        config,
        seed=seed,
        n_steps=config.max_steps,
        cars_per_step=config.cars_per_step,
        n_init_cars=config.init_cars,
    )

    eng = cityflow.Engine(f"{config.dir}/config.json", thread_num=1)
    road_lengths = create_road_length_dict(config)

    waiting_vehicles_percents = []
    car_distances = {}

    for step in range(config.max_steps):
        eng.next_step()
        # collect_data(eng, data_dict,reg_data,road_lengths)  # Used for the regression
        waiting_vehicles_percents.append(
            sum(eng.get_lane_waiting_vehicle_count().values())
            / eng.get_vehicle_count()
            * 100
        )

        for car_id in eng.get_vehicles(include_waiting=True):
            if car_id not in car_distances:
                vehicle_info = eng.get_vehicle_info(car_id)
                if vehicle_info["running"] == "1":
                    route = vehicle_info["route"]
                    route = route.split(" ")
                    car_distances[car_id] = sum(
                        road_lengths[road] for road in route[:-1]
                    )

        if verbose:
            print(f"At step {step+1}/{config.max_steps}", end="\r")
    if verbose:
        print("\n")

    # The max speed in manhattan is 40.2336
    average_freeflow_travel_time = np.mean(
        [distance / 40.2336 for distance in car_distances.values()]
    )
    travel_time_index = eng.get_average_travel_time() / average_freeflow_travel_time
    if verbose:
        print("------------------------Metrics:-------------------------")
        print("Average travel time = ", eng.get_average_travel_time())
        print("Free flow avg travel time = ", average_freeflow_travel_time)
        print("Average % waiting vehicles = ", np.mean(waiting_vehicles_percents[100:]))
        print("Travel Time Index = ", travel_time_index)

        sns.lineplot(
            x=list(range(len(waiting_vehicles_percents))), y=waiting_vehicles_percents
        )
        plt.ylabel("% waiting vehicles")
        plt.xlabel("time")
        plt.savefig(f"{config.dir}/waiting_vehicles.png")

    return SimpleNamespace(
        av_travel_time=eng.get_average_travel_time(),
        free_flow_travel_time=average_freeflow_travel_time,
        av_waiting_agents=np.mean(waiting_vehicles_percents[100:]),
        travel_time_index=travel_time_index,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default="low_manhattan")
    parser.add_argument("--max_steps", type=int, default=500)
    parser.add_argument("--cars_per_step", type=int, default=1)
    parser.add_argument("--init_cars", type=int, default=500)
    config = parser.parse_args()
    run_static_routing_simulation(config, verbose=True)
