import json
import math
from collections import defaultdict


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
                'coordinates': {'x': 123, 'y': 456},
                'connected_intersections': {
                    'connected_intersection_id2': 'connecting_road_id1',
                    'connected_intersection_id3': 'connecting_road_id2',
                    ....
                }
            }
            'intersection_id2': {
                'coordinates': {'x': 234, 'y': 567},
                'connected_intersections': {
                    'connected_intersection_id4': 'connecting_road_id3',
                    ....
                }
            }
            ....
        }

    :param config: namespace, consisting of the configuration for the simulation
    :returns: graph representing the roadnet
    """

    with open(f"{config.dir}/{config.dir}.json") as f:
        roadnet_json = json.load(f)

    graph = defaultdict(lambda: defaultdict(dict))
    for road in roadnet_json["roads"]:
        graph[road["startIntersection"]]["coordinates"] = road["points"][0]
        graph[road["startIntersection"]]["connected_intersections"][
            road["endIntersection"]
        ] = road["id"]
    return graph


def get_intersection_locations(config):
    """
    :param config: namespace, consisting of the configuration for the simulation
    :returns: dict with intersection ids as keys the roadnet
    """
    with open(f"{config.dir}/{config.dir}.json") as f:
        roadnet_json = json.load(f)

    return {
        intersection["id"]: {
            "x": intersection["point"]["x"],
            "y": intersection["point"]["y"],
        }
        for intersection in roadnet_json["intersections"]
    }


def get_road_intersections(config):
    """Given a configuration, returns a dictionary with for every road id its start and end
    intersection.

    :param config: namespace, consisting of the configuration for the simulation
    :returns: dict with intersection ids as keys the roadnet
    """
    with open(f"{config.dir}/{config.dir}.json") as f:
        roadnet_json = json.load(f)

    return {
        road["id"]: {
            "start_intersection": road["startIntersection"],
            "end_intersection": road["endIntersection"],
        }
        for road in roadnet_json["roads"]
    }


def collect_data(eng, data_dict, reg_data, road_lengths):
    all_vehicles_ids = eng.get_vehicles()
    lane_density = eng.get_lane_vehicle_count()
    for vehicle_id in all_vehicles_ids:
        vehicle_info = eng.get_vehicle_info(vehicle_id)
        if "road" in vehicle_info:
            if vehicle_id in data_dict.keys():
                if vehicle_info["running"] == "1":
                    if vehicle_info["road"] == data_dict[vehicle_id]["road_id"]:
                        data_dict[vehicle_id]["time_on_road"] += 1
                        for roads in lane_density:
                            if vehicle_info["road"] in roads:
                                cars_on_road = lane_density[roads]
                                break
                        else:
                            cars_on_road = 0
                        data_dict[vehicle_id]["cars_on_lane"].append(cars_on_road)
                    else:
                        if (
                            "211_0_1" in data_dict[vehicle_id]["road_id"]
                            or "327_0_1" in data_dict[vehicle_id]["road_id"]
                            or "177_0_1" in data_dict[vehicle_id]["road_id"]
                        ):
                            if data_dict[vehicle_id]["time_on_road"] > 0:
                                temp_list = []

                                road_len = road_lengths[
                                    data_dict[vehicle_id]["road_id"]
                                ]
                                avg_density = sum(
                                    data_dict[vehicle_id]["cars_on_lane"]
                                ) / len(data_dict[vehicle_id]["cars_on_lane"])
                                avg_density = avg_density / road_len

                                temp_list.append(avg_density)
                                temp_list.append(data_dict[vehicle_id]["time_on_road"])
                                print(temp_list)
                                reg_data.append(temp_list)

                        data_dict[vehicle_id]["road_id"] = vehicle_info["road"]
                        data_dict[vehicle_id]["time_on_road"] = 0
                        data_dict[vehicle_id]["cars_on_lane"] = []
                else:
                    pass
            else:
                data_dict[vehicle_id] = dict()
                data_dict[vehicle_id]["road_id"] = vehicle_info["road"]
                data_dict[vehicle_id]["time_on_road"] = 0
                data_dict[vehicle_id]["cars_on_lane"] = []
        else:
            pass
    return reg_data
