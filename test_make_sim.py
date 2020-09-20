import argparse
import cityflow
from utils import *
import types
from main_agent import create_random_vehicle
from agents import vehicle

MAX_STEPS = 100

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default='low_manhattan_sim')
    args = parser.parse_args()
    temp_config = types.SimpleNamespace(num_of_agents = 15, anchor_points = 1)

    vehicle_config = create_random_vehicle(temp_config)
    vehicles = [ vehicle(vehicle_config[i]) for i in range(0,temp_config.num_of_agents)]

    #eng = cityflow.Engine(f"{args.dir}/config.json", thread_num=1)
    eng = cityflow.Engine("low_manhattan_sim/config.json", thread_num=1)

    avg_travel_time = 0
    for step in range(MAX_STEPS):

        #Metrics
        vehicleCount = eng.get_vehicle_count()
        waitingVehiclesPerLane = eng.get_lane_waiting_vehicle_count()
        busyRoads = filterDicForZero(waitingVehiclesPerLane)
        averageTravelTime = eng.get_average_travel_time()
        vehicleIDs = eng.get_vehicles(include_waiting = True)


        #If there are no cars yet, this loop will be skipped
        for vvehicle in vehicleIDs:
            vehicleInfo = eng.get_vehicle_info(vvehicle)
            #vehicleInfo['running'] = '1' means that a car is on the map
            if vehicleInfo['running'] == '1':
                route = vehicleInfo['route']
                #Create an array where every element is a lane_ID of the route of a car
                route = route.split(' ')
                for lane in route:
                    if lane in busyRoads.keys():
                        print("Traffic jam at ", lane)

        print("\nStep", step, "\n")
        print("There are ", vehicleCount, " vehicles on the road now")

        avg_travel_time = avg_travel_time + eng.get_average_travel_time()

        eng.next_step()


    print("------------------------Metrics:-------------------------")
    print("Average travel time = ", avg_travel_time / MAX_STEPS)



if __name__ == "__main__":
    main()
