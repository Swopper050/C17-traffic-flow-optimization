import json
import math

def get_traffic_light_nodes(G):
    """
    Given a graph (as loaded with osmnx), returns all nodes with traffic lights. This is done
    using the degrees of the graph. If the degree is higher than 3, it is considered a traffic
    light node.

    :param G: Graph instance
    :returns: list of traffic light nodes
    """

    return [node for node in G.degree() if node[1] > 3]

def filterDicForZero(dic):
    newDic = dict()
    for key, value in dic.items():
        if value > 0:
            newDic[key] = value
    return newDic

def createRoadLengthDictionary():
    road_lengths = dict()
    with open('low_manhattan_sim/low_manhattan.json') as f:
        data = json.load(f)
    for road in data["roads"]:
        roadID = road["id"]
        x_start, x_end = road["points"][0]["x"], road["points"][1]["x"]
        y_start, y_end = road["points"][0]["y"], road["points"][1]["y"]
        length = math.sqrt( (x_start - x_end) * (x_start - x_end) + (y_start - y_end) * (y_start - y_end) )
        road_lengths[roadID] = length
    return road_lengths
