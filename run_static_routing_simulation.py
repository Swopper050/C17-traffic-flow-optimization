import argparse
import cityflow
from utils import create_road_length_dict
import json
import os
import numpy as np

from generate_random_cars_flow_file import generate_random_flow_file

def main(config):
    """ Runs a simulation using simple static routing.

    :param config: namespace with the configuration for the run
    """

    generate_random_flow_file(n_steps=config.max_steps, cars_per_step=config.cars_per_step, n_init_cars=config.init_cars)
    eng = cityflow.Engine(f"{config.dir}/config.json", thread_num=1)

    road_lengths = create_road_length_dict(config)
    car_distances = {}
    for step in range(1, config.max_steps + 1):

        #Calculate Metrics
        vehicle_count = eng.get_vehicle_count()
        waitingVehiclesPerLane = eng.get_lane_waiting_vehicle_count()

        for car_id in eng.get_vehicles(include_waiting = True):
            if car_id not in car_distances:
                vehicle_info = eng.get_vehicle_info(car_id)
                if vehicle_info["running"] == "1":
                    route = vehicle_info["route"]
                    route = route.split(" ")
                    car_distances[car_id] = sum(road_lengths[road] for road in route[:-1])

        print("\nStep", step, "/", config.max_steps, "\n", eng.get_average_travel_time())
        eng.next_step()

    # The max speed in manhattan is 40.2336
    average_freeflow_travel_time = np.mean([distance / 40.2336 for distance in car_distances.values()])
    travelTimeIndex = eng.get_average_travel_time() / average_freeflow_travel_time
    print("------------------------Metrics:-------------------")
    print("Average travel time = ", eng.get_average_travel_time())
    print("Free flow avg travel time", average_freeflow_travel_time)
    print("Travel Time Index = ", travelTimeIndex)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default='low_manhattan_sim')
    parser.add_argument("--max_steps", type=int, default=500)
    parser.add_argument("--cars_per_step", type=int, default= 1)
    parser.add_argument("--init_cars", type=int, default=500)
    config = parser.parse_args()
    main(config)
