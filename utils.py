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

    with open("low_manhattan_sim/low_manhattan.json") as f:
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
