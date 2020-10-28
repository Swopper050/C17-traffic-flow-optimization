import math

import numpy as np

from dynamic_route_planner import AV_MPS_SPEED, get_new_car_route

INTERSECTION_CHANGE_TIME_COST = 8
""" The average time/seconds/simulation steps it costs to traverse an intersection. """


class VehicleAgent:
    """ Class used to manage agents/vehicles. """

    def __init__(self, car_id, vehicle_info, *, t, max_steps, road_lengths):
        self.car_id = car_id
        self.max_steps = max_steps

        self.speed_over_time = []
        self.current_route = vehicle_info["route"].split(" ")[:-1]
        self.current_route_timing = self.estimate_route_timing(
            t, vehicle_info, road_lengths
        )

    def get_average_speed(self):
        """ Returns the average travel speed of this vehicle. """
        if len(self.speed_over_time) > 120:
            av_speed = np.mean(self.speed_over_time[:-120])
            return AV_MPS_SPEED if av_speed == 0.0 else av_speed
        return AV_MPS_SPEED  # If a car just started its route, assume average MPS speed

    def update_route(
        self, engine, current_t, central_system, vehicle_info, dynamic_router
    ):
        """Updates the route at this timestep for the current agent. Also lets the engine know the
        vehicle route changed (and which new route is taken).

        :param engine: the CityFlow engine
        :param current_t: current timestep of the simulation
        :param central_system: the Central System
        :param vehicle_info: information about the vehicle at the current timestep
        :param dynamic_router: DynamicRouter instance
        """

        self.speed_over_time.append(float(vehicle_info["speed"]))
        new_route = get_new_car_route(self, vehicle_info, dynamic_router)
        if new_route != self.current_route:
            dynamic_router.central_system.remove_route(
                self.car_id, self.current_route_timing
            )
            self.current_route = new_route
            new_route_timing = self.estimate_route_timing(
                current_t, vehicle_info, dynamic_router.road_lengths
            )
            dynamic_router.central_system.add_route(self.car_id, new_route_timing)
            engine.set_vehicle_route(self.car_id, self.current_route)

    def estimate_route_timing(self, current_t, vehicle_info, road_lengths):
        """
        Given the current route of the car, estimate at which timestep the car will be at which
        roads. This can be used to publish a route to the central system.

        :param current_t: current timestep (second) of the simulation
        :param vehicle_info: information about the vehicle at the current timestep
        :param road_lengths: dictionary with lengths of all roads in the map
        :returns: dictionary with for every road in the agents' current route a list of timesteps it
                  it expects to be on that road.
        """

        av_speed = self.get_average_speed()

        route_timing = {}
        offset = 0
        for road_id in self.current_route:

            road_length = road_lengths[road_id]
            if "road" in vehicle_info and road_id == vehicle_info["road"]:
                # Subtract distance on this road already traveled
                road_length -= float(vehicle_info["distance"])

            try:
                timesteps_on_road = int(road_length // av_speed)
            except Exception as e:
                import pdb

                pdb.set_trace()
            if (current_t + offset + timesteps_on_road) >= self.max_steps:
                timesteps_on_road = self.max_steps - (current_t + offset)

            route_timing[road_id] = [
                current_t + offset + t for t in range(timesteps_on_road)
            ]
            offset += timesteps_on_road + INTERSECTION_CHANGE_TIME_COST
        self.current_route_timing = route_timing
        return route_timing
