from astar import AStar
import numpy as np

from utils import create_road_length_dict, create_roadnet_graph


class Intersection:
    def __init__(self, id):
        self.id = id
        self.linked_roads = []
        self.linked_intersections = []


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

    def heuristic_cost_estimate(self, current, goal):
        """
        The heuristic for the Astar algorithm. The heuristic uses the distance between the
        intersections as well as the estimated traffic density.

        :param current: Intersection instance
        :param goal: Intersection instance
        :returns: float, heuristic cost estimate between the current and the goal
        """
        return float("inf")

    def distance_between(self, intersection1, intersection2):
        """
        Implements the distance between two nodes (intersections)

        :param intersection1: Intersection instance
        :param intersection2: Intersection instance
        :returns: the distance between the two nodes
        """
        raise NotImplementedError

    def neighbors(self, intersection):
        """
        Returns all neighbors (intersections) of the current node (intersection).

        :param intersection: Intersection instance
        :returns: list with id strings of all neighbors (intersections)
        """
        return intersection.linked_intersections


def get_new_car_route(car_id, vehicle_info, dynamic_router):
    """
    Given a specific car, updates the route of the car using the DynamicRoutePlanner, which takes
    into account both distance as well as expected traffic delay.

    :param car_id: id string of the car
    :param vehicle_info: dict with information about the car
    :param dynamic_router: initialized instance of DynamicRoutePlanner
    :returns: list with road_ids, the updated route for the car
    """
    return []
