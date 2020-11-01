from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from central_system import CentralSystem
from dynamic_route_planner import DynamicRoutePlanner, get_new_car_route
from vehicle_agent import VehicleAgent


class TestDynamicRoutePlanner:
    @pytest.fixture
    def config(self):
        return SimpleNamespace(
            dir="low_manhattan",
            max_steps=100,
            cars_per_step=1,
            init_cars=100,
        )

    @pytest.fixture
    def dynamic_router(self, config):
        return DynamicRoutePlanner(CentralSystem(config), config)

    @pytest.fixture
    def vehicle_agent(self):
        return VehicleAgent(
            "car1",
            {"route": "road1 road2"},
            t=0,
            max_steps=100,
            road_lengths={"road1": 10.0, "road2": 20},
        )

    def test_init(self, dynamic_router):
        assert dynamic_router.central_system is not None
        assert dynamic_router.road_lengths is not None
        assert dynamic_router.map_graph is not None
        assert dynamic_router.intersection_locs is not None
        assert dynamic_router.road_intersections is not None

        assert dynamic_router.current_t is None
        assert dynamic_router.road_densities_next_hour is None

    def test_prepare_astar(self, dynamic_router):
        dynamic_router.expected_road_travel_time = Mock(side_effect=[10.8, 12.6, 3.16])

        dynamic_router.road_lengths = {
            "road1": 100,
            "road2": 120,
            "road3": 15,
        }
        dynamic_router.prepare_astar(5)

        assert dynamic_router.current_t == 5
        assert dynamic_router.road_travel_times == {
            "road1": 10.8,
            "road2": 12.6,
            "road3": 3.16,
        }

    def test_heuristic_cost_estimate(self, dynamic_router):
        dynamic_router.intersection_locs = {
            "intersection1": {"x": 10, "y": 20},
            "intersection2": {"x": 15, "y": 25},
        }

        cost = dynamic_router.heuristic_cost_estimate("intersection1", "intersection2")
        assert round(cost, 3) == 3.074

    def test_distance_between(self, dynamic_router):
        dynamic_router.map_graph = {
            "intersection1": {"connected_intersections": {"intersection2": "road1"}},
        }
        dynamic_router.road_travel_times = {
            "road1": 20.5,
            "road2": 10.1,
        }

        assert dynamic_router.distance_between("intersection1", "intersection2") == 20.5

    def test_neighbors(self, dynamic_router):
        dynamic_router.map_graph = {
            "intersection1": {
                "connected_intersections": {
                    "intersection2": "road1",
                    "intersection3": "road2",
                    "intersection5": "road3",
                }
            },
        }
        assert dynamic_router.neighbors("intersection1") == [
            "intersection2",
            "intersection3",
            "intersection5",
        ]

    def test_expected_road_travel_time(self, dynamic_router):
        dynamic_router.road_lengths = {"road1": 20}
        central_system_mock = Mock()
        central_system_mock.get_density_at_interval.return_value = {
            2: 5,
            3: 5,
            4: 6,
            5: 6,
            6: 3,
        }
        dynamic_router.central_system = central_system_mock

        travel_time = dynamic_router.expected_road_travel_time("road1", 2)
        assert round(travel_time, 3) == 18.696

    def test_get_start_end_intersection(self, dynamic_router):
        dynamic_router.road_intersections = {
            "road1": {
                "start_intersection": "intersection1",
                "end_intersection": "intersection2",
            },
            "road2": {
                "start_intersection": "intersection3",
                "end_intersection": "intersection4",
            },
            "road3": {
                "start_intersection": "intersection4",
                "end_intersection": "intersection2",
            },
            "road4": {
                "start_intersection": "intersection5",
                "end_intersection": "intersection6",
            },
        }

        assert dynamic_router.get_start_end_intersection("road1", "road4") == (
            "intersection2",
            "intersection6",
        )

    def test_get_route_from_solution(self, dynamic_router):
        dynamic_router.map_graph = {
            "intersection1": {"connected_intersections": {"intersection2": "road1"}},
            "intersection2": {
                "connected_intersections": {
                    "intersection3": "road2",
                    "intersection4": "road3",
                }
            },
            "intersection3": {
                "connected_intersections": {
                    "intersection4": "road4",
                    "intersection5": "road5",
                }
            },
        }

        roads = dynamic_router.get_route_from_solution(
            ["intersection1", "intersection2", "intersection3", "intersection5"]
        )
        assert roads == ["road1", "road2", "road5"]

    def test_get_new_car_route(self, vehicle_agent):
        vehicle_agent.current_route = ["road1", "road2", "road3", "road4"]

        router_mock = Mock()
        router_mock.get_start_end_intersection.return_value = (
            "intersection1",
            "intersection4",
        )
        router_mock.get_route_from_solution.return_value = ["road5", "road6", "road4"]
        new_route = get_new_car_route(vehicle_agent, {"road": "road1"}, router_mock)

        router_mock.get_start_end_intersection.assert_called_once_with("road1", "road4")
        router_mock.astar.assert_called_once_with("intersection1", "intersection4")
        assert new_route == ["road1", "road5", "road6", "road4"]

    def test_get_new_car_route_last_route(self, dynamic_router, vehicle_agent):
        vehicle_agent.current_route = ["road1"]

        # Last road can't change
        assert get_new_car_route(vehicle_agent, None, dynamic_router) == ["road1"]
