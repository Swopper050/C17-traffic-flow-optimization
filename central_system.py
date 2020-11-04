import json


class CentralSystem:
    """
    Class which acts as the central system. Can be used by agents to communicate about the state
    of the environment, publish routes to with expected travel times and remove previously
    published routes.

    Can be thought of as a map over time which keeps track of traffic density for every road.
    """

    def __init__(self, config):
        """Intializes the central system using the given config.

        :param config: namespace with the configuration
        """
        self.config = config
        self.map_density_over_time = {}

    def add_route(self, car_id, route_dict):
        """
        This function can be used to add the route of a car such that the central system knows
        at which time the car expects to be at which road.

        :param car_id: str, car id
        :param route_dict: a dictionary with road ids as keys and list of timesteps to be there

        :Example:

            >>> road_dict = {
            >>>     "road_id1": [t12, t13, t14],
            >>>     "road_id2": [t15, t16],
            >>>     "road_id5": [t17, t18, t19, t20]
            >>> }
            >>> car_id = "car1"
            >>> central_system.add_route(car_id, road_dict)
        """

        for road_id, timesteps in route_dict.items():
            for t in timesteps:
                self.map_density_over_time[road_id][t].append(car_id)

    def remove_route(self, car_id, route_dict):
        """
        This function can be used to remove an added route of a car from the central system.
        This can happen when a car changes route for example.

        :param car_id: str, car id
        :param route_dict: a dictionary with road ids as keys and list of timesteps to be there

        :Example:

            >>> road_dict = {
            >>>     "road_id1": [t12, t13, t14],
            >>>     "road_id2": [t15, t16],
            >>>     "road_id5": [t17, t18, t19, t20]
            >>> }
            >>> car_id = "car2"
            >>> central_system.remove_route(car_id, road_dict)
        """

        try:
            for road_id, timesteps in route_dict.items():
                for t in timesteps:
                    self.map_density_over_time[road_id][t].remove(car_id)
        except Exception as e:
            print(f"Route to be removed was not found in the central system.. {e}")

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
            for t in range(min_t, min(self.config.max_steps, max_t))
        }

    def init_map_density(self):
        """ Initializes the map density over time. """
        with open(f"{self.config.dir}/{self.config.dir}.json") as data_file:
            data = json.load(data_file)
            for road in data["roads"]:
                self.map_density_over_time[road["id"]] = [
                    [] for _ in range(self.config.max_steps)
                ]
