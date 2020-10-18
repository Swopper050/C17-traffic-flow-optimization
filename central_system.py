import json


class CentralSystem:
    """
    Docs about the central system: TODO
    """

    def __init__(self, config):
        """ Intializes the central system using the given config.

        :param config: namespace with the configuration
        """
        self.config = config
        self.map_density_over_time = {}

        with open(f"{config.dir}.json") as data_file:
            data = json.load(data_file)
            for road in data["roads"]:
                self.map_density_over_time[road["id"]] = [[] for _ in range(config.max_steps)]

    def add_route(self, car_id, route_dict):
        """
        This function can be used to add the route of a car such that the central system knows
        at which time the car expects to be at which road.

        :param car_id: str, car id
        :param route_dict: a dictionary as follows:
            {
                "road_id1": [t12, t13, t14],
                "road_id2": [t15, t16],
                "road_id5": [t17, t18, t19, t20],
            }
        """

        for road_id, timesteps in route_dict.items():
            for t in timesteps:
                self.map_density_over_time[road_id][t].append(car_id)

    def remove_route(self, car_id, route_dict):
        """
        This function can be used to remove an added route of a car from the central system.
        This can happen when a car changes route for example.

        :param car_id: str, car id
        :param route_dict: a dictionary as follows:
            {
                "road_id1": [t12, t13, t14],
                "road_id2": [t15, t16],
                "road_id5": [t17, t18, t19, t20],
            }
        """

        try:
            for road_id, timesteps in route_dict.items():
                for t in timesteps:
                    self.map_density_over_time[road_id][t].remove(car_id)
        except Exception:
            print("Route to be removed was not found in the central system..")

    def get_density_at_interval(self, road_id, min_t, max_t):
        """
        This function can be used to request the density of a road at a given interval. The density
        is simply the number of cars on that road at a specific time.

        :param road_id: str, id of the road
        :param min_t: start of the time interval
        :param max_t: end of the time interval
        :returns: a dictionary with for every timestep in the interval the density
        """

        return {
            t: len(self.map_density_over_time[road_id][t])
            for t in range(min_t, max_t)
        }
