import argparse
from collections import defaultdict
import json
import os

import cityflow
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from utils import create_road_length_dict
from vehicle_agent import VehicleAgent

sns.set_theme()

from astar_routing import DynamicRoutePlanner, get_new_car_route
from generate_random_cars_flow_file import generate_random_flow_file


def run_dynamic_routing_simulation(config):
    """Runs a simulation using dynamic routing.
    NOTE: This function is under construction! It does not work yet

    :param config: namespace with the configuration for the run
    """

    generate_random_flow_file(
        config,
        n_steps=config.max_steps,
        cars_per_step=config.cars_per_step,
        n_init_cars=config.init_cars,
    )
    eng = cityflow.Engine(f"{config.dir}/config.json", thread_num=1)

    road_lengths = create_road_length_dict(config)
    central_system = None  # TODO
    dynamic_router = DynamicRoutePlanner(central_system, config)

    neighbors = dynamic_router.neighbors("42427369")
    print(dynamic_router.distance_between("42427369", neighbors[0]))
    print(dynamic_router.distance_between("42427369", neighbors[1]))

    agents = {}
    car_distances = {}
    waiting_vehicles_percents = []
    for step in range(config.max_steps):
        eng.next_step()

        n_vehicles = eng.get_vehicle_count()
        if n_vehicles > 0:
            waiting_vehicles_percents.append(
                sum(eng.get_lane_waiting_vehicle_count().values())
                / eng.get_vehicle_count()
                * 100
            )
        else:
            waiting_vehicles_percents.append(0.0)

        for car_id in eng.get_vehicles(include_waiting=True):
            if car_id not in car_distances:
                vehicle_info = eng.get_vehicle_info(car_id)
                if vehicle_info["running"] == "1":
                    route = vehicle_info["route"]
                    route = route.split(" ")
                    car_distances[car_id] = sum(
                        road_lengths[road] for road in route[:-1]
                    )

        for car_id in eng.get_vehicles(include_waiting=True):
            vehicle_info = eng.get_vehicle_info(car_id)
            if vehicle_info["running"] == "1":
                if car_id not in agents:
                    agents[car_id] = VehicleAgent(car_id, route=vehicle_info["route"])

                agent = agents[car_id]
                route_timing = agent.estimate_route_timing(step, vehicle_info, road_lengths)
                central_system.add_route(car_id, route_timing)
                import pdb; pdb.set_trace()
                agent.update_route(vehicle_info, dynamic_router, central_system)
                eng.set_vehicle_route(car_id, agent.current_route)


        print(f"At step {step+1}/{config.max_steps}", end="\r")
    print("\n")

    # The max speed in manhattan is 40.2336
    average_freeflow_travel_time = np.mean(
        [distance / 40.2336 for distance in car_distances.values()]
    )
    travel_time_index = eng.get_average_travel_time() / average_freeflow_travel_time
    print("------------------------Metrics:-------------------------")
    print("Average travel time = ", eng.get_average_travel_time())
    print("Free flow avg travel time = ", average_freeflow_travel_time)
    print("Average % waiting vehicles = ", np.mean(waiting_vehicles_percents[100:]))
    print("Travel Time Index = ", travel_time_index)

    sns.lineplot(
        x=list(range(len(waiting_vehicles_percents))), y=waiting_vehicles_percents
    )
    plt.ylabel("% waiting vehicles")
    plt.xlabel("t")
    plt.savefig(f"{config.dir}/waiting_vehicles.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default="low_manhattan")
    parser.add_argument("--max_steps", type=int, default=500)
    parser.add_argument("--cars_per_step", type=int, default=1)
    parser.add_argument("--init_cars", type=int, default=500)
    config = parser.parse_args()
    run_dynamic_routing_simulation(config)
