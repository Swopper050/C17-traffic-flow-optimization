from collections import defaultdict
import json
import math


def filterDicForZero(dic):
    newDic = dict()
    for key, value in dic.items():
        if value > 0:
            newDic[key] = value
    return newDic


def create_road_length_dict(config):
    """
    Given a certain configuration, creates a dictionary with for every road in the
    roadnet the corresponding length in meters.

    :param config: namespace with configuration for the simulation folder
    :returns: dictionary with road_ids as keys and lengths as values
    """

    with open(f"{config.dir}/{config.dir}.json") as f:
        data = json.load(f)

    road_lengths = dict()
    for road in data["roads"]:
        roadID = road["id"]
        x_start, x_end = road["points"][0]["x"], road["points"][1]["x"]
        y_start, y_end = road["points"][0]["y"], road["points"][1]["y"]
        road_lengths[roadID] = math.sqrt(
            (x_start - x_end) ** 2 + (y_start - y_end) ** 2
        )

    return road_lengths


def create_roadnet_graph(config):
    """
    Given a configuration namespace as needed for a simulation, builds the roadnet in graph form,
    considering intersections as nodes and roads as edges. The graph will be represented as a
    dictionary constructed as follows:
        graph = {
            'intersection_id1': {
                'connected_intersection_id2': 'connecting_road_id1',
                'connected_intersection_id3': 'connecting_road_id2',
                ....
            }
            'intersection_id2': {
                'connected_intersection_id4': 'connecting_road_id3',
                ....
            }
            ....
        }

    :param config: namespace, consisting of the configuration for the simulation
    :returns: graph representing the roadnet
    """

    with open(f"{config.dir}/{config.dir}.json") as f:
        roadnet_json = json.load(f)

    graph = defaultdict(dict)
    for road in roadnet_json["roads"]:
        graph[road["startIntersection"]][road["endIntersection"]] = road["id"]
    return graph
