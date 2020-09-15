import argparse
from agents import vehicle, update_flow_json
import pdb
def main():
    parser = argparse.ArgumentParser(
        description="Create vehicle class objects"
    )
    parser.add_argument('-l', '--length',
                        type=float,
                        default=5.0,
                        help='Length of vehicle')
    parser.add_argument('-w', '--width',
                        type=float,
                        default=2.0,
                        help='Width of vehicle')
    parser.add_argument('-ma', '--max_acc',
                        type=float,
                        default=2.0,
                        help='Maximum Acceleration of vehicle')
    parser.add_argument('-md', '--max_dec',
                        type=float,
                        default=4.5,
                        help='Maximum Deceleration of vehicle')
    parser.add_argument('-ua', '--usual_acc',
                        type=float,
                        default=2.0,
                        help='Usual acceleration of the vehicle')
    parser.add_argument('-ud', '--usual_deceleration',
                        type=float,
						default=4.5,
						help='Usual deceleration of the Vehicle')
    parser.add_argument('-mg', '--min_gap',
					    type=float,
                        default=2.5,
                        help='Minimum gap between two Vehicles')
    parser.add_argument('-ms', '--max_speed',
                        type=float,
                        default=16.67,
                        help='Maximum speed of the Vehicle')
    parser.add_argument('-ht', '--headway_time',
                        type=float,
                        default=1.5,
                        help='Minimum Headway time between two vehicles')
    parser.add_argument('-i', '--interval',
                        type=float,
                        default=2.0,
                        help='Interval to add new Vehicle to simulation')
    parser.add_argument('-st', '--start_time',
                        type=int,
                        default=0,
                        help='Start time to add new Vehicles')
    parser.add_argument('-et', '--end_time',
                        type=int,
                        default=-1,
                        help='End time to stop adding new Vehicles')
    parser.add_argument('-r', '--route',
                        type=list,
                        default=[],
                        help='Source, destination and anchor points to traverse')
	
    config = parser.parse_args()
    update_flow_json()
	

if __name__ == '__main__':
	main()