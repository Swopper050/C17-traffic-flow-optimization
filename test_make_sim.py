import argparse
import cityflow
from utils import *
import types
import pdb
from main_agent import create_random_vehicle
from agents import vehicle
import json
import os
from os import path


MAX_STEPS = 1000
BUSY_ROAD_THRESHOLD = 4


def main():
    #Test
    #Delete the low_manhattan_flow.json file
    if path.exists("low_manhattan_sim/low_manhattan_flow.json"):
        os.remove("low_manhattan_sim/low_manhattan_flow.json")
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default='low_manhattan_sim')
    args = parser.parse_args()
    temp_config = types.SimpleNamespace(num_of_agents = 10, anchor_points = 1)
    vehicle_config = create_random_vehicle(temp_config)
    vehicles = [ vehicle(vehicle_config[i]) for i in range(0,temp_config.num_of_agents)]


    eng = cityflow.Engine("low_manhattan_sim/config.json", thread_num=1)
    avg_travel_time = 0

    road_lengths = createRoadLengthDictionary()
    for step in range(1, MAX_STEPS + 1):

        #Calculate Metrics
        vehicleCount = eng.get_vehicle_count()
        waitingVehiclesPerLane = eng.get_lane_waiting_vehicle_count()
        busyRoads = filterDicForZero(waitingVehiclesPerLane)
        vehicleIDs = eng.get_vehicles(include_waiting = True)

        #If there are no cars yet, this loop will be skipped
        for car in vehicleIDs:
            continue
            vehicleInfo = eng.get_vehicle_info(car)
            #vehicleInfo['running'] = '1' means that a car is on the map
            if vehicleInfo['running'] == '1':
                route = vehicleInfo['route'].split(' ')
                del route[-1]
                if route[-1] == vehicleInfo['road']:
                    print("Destination reached")


        print("\nStep", step, "/", MAX_STEPS, "\n")


        eng.next_step()

    car_distance = dict()
    for car in vehicleIDs:
        vehicleInfo = eng.get_vehicle_info(car)
        distance = 0
        #Not sure what running is actually, cant find anything.
        if vehicleInfo['running'] == '1':
            route = vehicleInfo['route']
            route = route.split(' ')
            del route[-1]
            for lane in route:
                distance = distance + road_lengths[lane]
            car_distance[car] = distance


    avg_travel_time = eng.get_average_travel_time()
    print("------------------------Metrics:-------------------------")
    print("Average travel time = ", avg_travel_time / MAX_STEPS)
    print("car_distances = ", car_distance)




if __name__ == "__main__":
    main()
