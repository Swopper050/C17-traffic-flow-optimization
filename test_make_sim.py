import argparse
import cityflow
from utils import *

MAX_STEPS = 1000

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default='low_manhattan_sim')
    args = parser.parse_args()
    eng = cityflow.Engine(f"{args.dir}/config.json", thread_num=1)
    for step in range(MAX_STEPS):
        print("\nStep", step, "\n")

        #Metrics
        vehicleCount = eng.get_vehicle_count()
        waitingVehiclesPerLane = eng.get_lane_waiting_vehicle_count()
        busyRoads = filterDicForZero(waitingVehiclesPerLane)
        averageTravelTime = eng.get_average_travel_time()
        vehicleIDs = eng.get_vehicles(include_waiting = True)
        
        print("There are ", vehicleCount, " vehicles on the road now")

        #If there are no cars on the map, this loop will be skipped
        for vehicle in vehicleIDs:
            vehicleInfo = eng.get_vehicle_info(vehicle)
            if vehicleInfo['running'] == '1':
                route = vehicleInfo['route']
                #Create an array where every element is a lane_ID of the route of a car
                route = route.split(' ')
                for lane in route:
                    if lane in busyRoads.keys():
                        print("Traffic jam at ", lane)


        eng.next_step()

if __name__ == "__main__":
    main()
