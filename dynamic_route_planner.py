import json
import math

import numpy as np
from astar import AStar

from utils import create_road_length_dict, create_roadnet_graph, get_intersection_locations

AV_MPS_SPEED = 2.3


class DynamicRoutePlanner(AStar):
    """
    A variant based on Astar which finds the optimal route taking into consideration the
    expected traffic delays.
    """

    def __init__(self, central_system, config):
        """
        :param central_system: the central system usable by agents to get traffic states
        :param road_lengths: dictionary with as keys road ids and as values their lengths
        :param map_graph: the map represented as a graph, nodes are intersections, edges are roads.
        """
        self.central_system = central_system
        self.road_lengths = create_road_length_dict(config)
        self.map_graph = create_roadnet_graph(config)
        self.intersection_locs = get_intersection_locations(config)

        self.current_t = None
        self.road_densities_next_hour = None

    def prepare_astar(self, current_t):
        """Sets attributes for the astar algorithm to work properly. Needs to be called once every
        step of the simulation.

        :param current_t: the time/step of the simulation when doing the astar search
        """
        self.current_t = current_t
        self.road_travel_times = {
            road_id: self.expected_road_travel_time(road_id, current_t)
            for road_id in self.road_lengths.keys()
        }

    def heuristic_cost_estimate(self, current_intersection_id, goal_intersection_id):
        """
        The heuristic for the Astar algorithm. The heuristic uses simply the euclidean distance
        between the current intersection and the goal intersection. Converses it to travel time
        by dividing it by the average travel speed of the agents.

        :param current_intersection_id: id string of the current intersection
        :param goal_intersection_id: id string of the goal intersection
        :returns: float, heuristic cost estimate between the current and the goal
        """
        import pdb; pdb.set_trace()
        current_coordinates = self.map_graph[current_intersection_id]["coordinates"]
        goal_coordinates = self.map_graph[goal_intersection_id]["coordinates"]
        import pdb; pdb.set_trace()
        curr_x, curr_y = current_coordinates["x"], current_coordinates["y"]
        goal_x, goal_y = goal_coordinates["x"], goal_coordinates["y"]
        return math.sqrt((curr_x - goal_x) ** 2 + (curr_y - goal_y) ** 2) / AV_MPS_SPEED

    def distance_between(self, intersection_id1, intersection_id2):
        """
        Implements the distance between two nodes (intersections). The 'cost' of a road is the
        distance combined with the expect traffic density at the time the road will be traversed.

        :param intersection_id1: id string of the first intersection
        :param intersection_id2: id string of the second intersection
        :returns: the distance between the two nodes
        """
        corresponding_road = self.map_graph[intersection_id1][
            "connected_intersections"
        ][intersection_id2]
        return self.road_travel_times[corresponding_road]

    def neighbors(self, intersection_id):
        """
        Returns all neighbors (intersections) of the current node (intersection).

        :param intersection: id string of the intersection
        :returns: list with id strings of all neighbors (intersections)
        """
        return list(self.map_graph[intersection_id]["connected_intersections"].keys())

    def expected_road_travel_time(self, road_id, t):
        """
        Calculates the expected time it takes currently to traverse the given road.

        :param road_id: id of the road
        :param t: current timestep of the simulation
        """
        length = self.road_lengths[road_id]
        normal_traverse_time = length / AV_MPS_SPEED
        road_density = self.central_system.get_density_at_interval(road_id, t, t + 30)
        av_density = np.mean(list(road_density.values()))
        return normal_traverse_time + av_density * 2

def get_new_car_route(vehicle_agent, vehicle_info, dynamic_router):
    """
    Given a specific car, updates the route of the car using the DynamicRoutePlanner, which takes
    into account both distance as well as expected traffic delay.

    :param vehicle_agent: VehicleAgent instance
    :param vehicle_info: dict with information about the car
    :param dynamic_router: initialized instance of DynamicRoutePlanner
    :returns: list with road_ids, the updated route for the car
    """

    current_idx_in_route = vehicle_agent.current_route.index(vehicle_info["road"])
    solution = dynamic_router.astar(vehicle_info["road"], vehicle_agent.current_route[-1])
    new_route = vehicle_agent.current_route[:current_idx_in_route]
    import pdb; pdb.set_trace()
    return new_route
