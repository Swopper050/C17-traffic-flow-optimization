import argparse
import cityflow

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default='low_manhattan_sim')
    args = parser.parse_args()
    eng = cityflow.Engine(f"{args.dir}/config.json", thread_num=1)
    for step in range(100):
        print("\nStep", step, "\n")


        vehicleCount = eng.get_vehicle_count()
        waitingVehiclesPerLane = eng.get_lane_waiting_vehicle_count()
        averageTravelTime = eng.get_average_travel_time()
        vehicleIDs = eng.get_vehicles(include_waiting = True)
        print("There are ", vehicleCount, " on the road now")

        #If there are no cars on the map, this loop will be skipped
        for vehicle in vehicleIDs:
            vehicleInfo = eng.get_vehicle_info(vehicle)
            if vehicleInfo['running'] != '0':
                route = vehicleInfo['route']
                #Create an array where every element is a lane_ID of the route of a car
                route = route.split(' ')
                for lane in route:
                    if lane in waitingVehiclesPerLane:
                        print("I might have an conjegtion")

        eng.next_step()
