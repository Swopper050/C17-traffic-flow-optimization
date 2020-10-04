import argparse
import cityflow
from utils import create_road_length_dict
import json
import os
import numpy as np

from generate_random_cars_flow_file import generate_random_flow_file


MAX_STEPS = 500
BUSY_ROAD_THRESHOLD = 4


def main(config):
    """ Runs a simulation using simple static routing.

    :param config: namespace with the configuration for the run
    """

    generate_random_flow_file(n_steps=MAX_STEPS, cars_per_step=1, n_init_cars=300)
    eng = cityflow.Engine(f"{config.dir}/config.json", thread_num=1)

    road_lengths = create_road_length_dict(config)
    car_distances = {}
    for step in range(1, MAX_STEPS + 1):

        #Calculate Metrics
        vehicleCount = eng.get_vehicle_count()
        waitingVehiclesPerLane = eng.get_lane_waiting_vehicle_count()

        for car_id in eng.get_vehicles(include_waiting = True):
            if car_id not in car_distances:
                vehicle_info = eng.get_vehicle_info(car_id)
                if vehicle_info["running"] == "1":
                    route = vehicle_info["route"]
                    route = route.split(" ")
                    car_distances[car_id] = sum(road_lengths[road] for road in route[:-1])

        print("\nStep", step, "/", MAX_STEPS, "\n", eng.get_average_travel_time())
        eng.next_step()

    # The max speed in manhattan is 40.2336
    average_freeflow_travel_time = np.mean([distance / 40.2336 for distance in car_distances.values()])
    print("------------------------Metrics:-------------------------")
    print("Average travel time = ", eng.get_average_travel_time())
    print("Free flow avg travel time", average_freeflow_travel_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default='low_manhattan_sim')
    config = parser.parse_args()
    main(config)
