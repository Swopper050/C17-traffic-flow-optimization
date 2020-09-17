import argparse
import cityflow

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default='low_manhattan_sim')
    args = parser.parse_args()
    eng = cityflow.Engine(f"{args.dir}/config.json", thread_num=1)
    for i in range(100):
        vehicleCount = eng.get_vehicle_count()
        waitingTimePerLane = eng.get_lane_waiting_vehicle_count()
        averageTravelTime = eng.get_average_travel_time()
        vehicleIDs = eng.get_vehicles(include_waiting = True)
        if vehicleCount > 0:

            for vehicle in vehicleIDs:
                vehicleInfo = eng.get_vehicle_info(vehicle)
                if vehicleInfo['running'] != '0':
                    if float(vehicleInfo['speed']) < 0.4:
                        print('Car', vehicleID, 'is standing still at intersection', vehicleInfo['intersection'])

        eng.next_step()
