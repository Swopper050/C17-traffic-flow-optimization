'''
This is the main file from which agent objects can be created.
'''

import argparse
from agents import vehicle
import pdb
import random
import types
import json

#Thisfunction generates random values for vehicle properties
def create_random_vehicle(config):
	sim_config = list()
	with open("./low_manhattan_sim/low_manhattan.json") as f:
		roadnet_json = json.load(f)

	#Check if road ids are present in roadnet json
#	if ('static' not in roadnet_json) or  \
#		 ( 'edges' not in roadnet_json['static']) or \
##		raise Exception("Roadnet.json does not sufficient data to initialise vehicles")

	#Add road ids from roadnet json to route attribute of class
	# Based on input, 2 or 3 road indices from roadnet json	are stored and added to self.route
	for i in range(0, config.num_of_agents):
		road_index = []
		while(len(road_index) < config.anchor_points + 1):
			random_index = random.randint(0,len(roadnet_json['roads']) - 1)
			if random_index in road_index:
				pass
			else:
				road_index.append(random_index)
		'''
		Add code for random intersection
		'''
		#Create a namespace object to
		temp_config = types.SimpleNamespace(
			length = round(random.uniform(4,6),1),
			#width = length / 2.5,
			maxPosAcc = round(random.uniform(1,4),1),
			maxNegAcc = round(random.uniform(4,7),1),
			#usualPosAcc = maxPosAcc / 2,
			#usualNegAcc = maxNegAcc / 2,
			minGap = round(random.uniform(0.5,3),1),
			maxSpeed = round(random.uniform(10,50),2),
			headwayTime = round(random.uniform(1,3),1),
			route = [ roadnet_json['roads'][index]['id'] for index in road_index],
			interval = 5.0,
			startTime = 0,
			endTime = -1
			)
		sim_config.append(temp_config)
	return sim_config

def main():

	parser = argparse.ArgumentParser(
		description="Create vehicle class objects"
		)

	'''
	This section can be used if input is given manually and not randomly
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
    parser.add_argument('-ud', '--usual_dec',
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
    '''
	parser.add_argument('-n', '--num_of_agents',
                        type=int,
                        default=2,
                        help='Number of distinct vehicles to generate')
	parser.add_argument('-a', '--anchor_points',
                        type=int,
                        default=2,
                        help="Source to destination route. Value '1': Shortest Path. Value '2': Through 1 randomly chosen road. Value '3': Through 1 randomly chosen intersection.")
	config = parser.parse_args()
	vehicle_config = create_random_vehicle(config)
	vehicles = [ vehicle(vehicle_config[i]) for i in range(0,config.num_of_agents)]

if __name__ == '__main__':
	main()
