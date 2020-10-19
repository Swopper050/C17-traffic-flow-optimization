import numpy as np

from astar_routing import get_new_car_route


class VehicleAgent:
    """ Class used to manage agents/vehicles. """

    def __init__(self, car_id, *, route):
        self.car_id = car_id
        self.speed_over_time = []
        self.current_route = route.split(" ")[:-1]

    def get_average_speed(self):
        """ Returns the average travel speed of this vehicle. """
        if len(self.speed_over_time) > 120:
            return np.mean(self.speed_over_time[:-120])
        return 7  # If a car just started driving, assume around 7 m/s

    def update_route(self, vehicle_info, dynamic_router):
        """ Updates the route at this timestep for the current agent and the current state
        of the central system.

        :param vehicle_info: information about the vehicle at the current timestep
        :param dynamic_router: DynamicRouter instance
        """

        self.speed_over_time.append(vehicle_info["speed"])
        get_new_car_route(self.car_id, vehicle_info, dynamic_router)

    def estimate_route_timing(self, current_t, max_steps, vehicle_info, road_lengths):
        """
        Given the current route of the car, estimate at which timestep the car will be at which
        roads. This can be used to publish a route to the central system.

        :param current_t: current timestep (second) of the simulation
        :param max_steps: maximum number of steps in the simulation
        :param vehicle_info: information about the vehicle at the current timestep
        :param road_lengths: dictionary with lengths of all roads in the map
        :returns: dictionary with for every road in the agents' current route a list of timesteps it
                  it xpects to be on that road.
        """

        av_speed = self.get_average_speed()

        route_timing = {}
        offset = 0
        for road_id in self.current_route:

            road_length = road_lengths[road_id]
            if road_id == vehicle_info["road"]:
                road_length -= float(vehicle_info["distance"])

            timesteps_on_road = int(road_length // av_speed)
            if (current_t + offset + timesteps_on_road) >= max_steps:
                timesteps_on_road = max_steps - (current_t + offset)

            route_timing[road_id] = [current_t + offset + t for t in range(timesteps_on_road)]
            offset += timesteps_on_road
        return route_timing
