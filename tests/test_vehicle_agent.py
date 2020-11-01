from unittest.mock import Mock

import pytest

from dynamic_route_planner import AV_MPS_SPEED
from vehicle_agent import VehicleAgent


class TestVehicleAgent:
    @pytest.fixture
    def road_lengths(self):
        return {
            "road1": 10,
            "road2": 20,
            "road3": 30,
            "road4": 15,
        }

    @pytest.fixture
    def agent(self, road_lengths):
        return VehicleAgent(
            "car1",
            {"route": "road1 road2 road3 "},
            t=0,
            max_steps=100,
            road_lengths=road_lengths,
        )

    def test_init(self, agent):
        assert agent.car_id == "car1"
        assert agent.max_steps == 100
        assert agent.speed_over_time == []
        assert agent.current_route == ["road1", "road2", "road3"]
        assert agent.current_route_timing == {
            "road1": [0, 1, 2, 3],
            "road2": [12, 13, 14, 15, 16, 17, 18, 19],
            "road3": [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
        }

    def test_get_average_speed_not_enough_data(self, agent):
        assert agent.get_average_speed() == AV_MPS_SPEED

    def test_get_average_speed(self, agent):
        agent.speed_over_time = [5] * 100 + [6] * 100

        # Average is of the last 120 timesteps: (20 * 5 + 100 * 6) / 120 == 5.83
        assert round(agent.get_average_speed(), 2) == 5.83

    def test_update_route(self, agent, road_lengths, monkeypatch):
        engine = Mock()
        first_route_timing = agent.current_route_timing

        get_new_car_route_mock = Mock(return_value=["road1", "road2", "road4"])
        monkeypatch.setattr("vehicle_agent.get_new_car_route", get_new_car_route_mock)

        t = 1
        central_system_mock = Mock()
        vehicle_info = {"speed": 4}
        dynamic_router_mock = Mock()
        dynamic_router_mock.road_lengths = road_lengths
        dynamic_router_mock.central_system = central_system_mock

        new_route_timing = {
            "road1": [1, 2, 3, 4],
            "road2": [13, 14, 15, 16, 17, 18, 19, 20],
            "road4": [29, 30, 31, 32, 33, 34],
        }

        agent.update_route(engine, t, vehicle_info, dynamic_router_mock)

        assert agent.speed_over_time == [4]
        get_new_car_route_mock.assert_called_once_with(
            agent, vehicle_info, dynamic_router_mock
        )
        central_system_mock.remove_route.assert_called_once_with(
            "car1", first_route_timing
        )

        assert agent.current_route == ["road1", "road2", "road4"]
        assert agent.current_route_timing == new_route_timing

        central_system_mock.add_route.assert_called_once_with("car1", new_route_timing)
        engine.set_vehicle_route.assert_called_once_with("car1", agent.current_route)

    def test_estimate_route_timing(self, agent, road_lengths):
        vehicle_info = {
            "road": "road1",
            "distance": 2,
        }

        agent.current_route = ["road1", "road2"]
        route_timing = agent.estimate_route_timing(3, vehicle_info, road_lengths)

        assert route_timing == {
            "road1": [3, 4, 5],
            "road2": [14, 15, 16, 17, 18, 19, 20, 21],
        }

    def test_estimate_route_timing_route_too_long(self, agent, road_lengths):
        vehicle_info = {
            "road": "road1",
            "distance": 0,
        }

        agent.current_route = ["road1"]

        agent.max_steps = 3
        route_timing = agent.estimate_route_timing(0, vehicle_info, road_lengths)
        assert route_timing == {"road1": [0, 1, 2]}

        agent.max_steps = 4
        route_timing = agent.estimate_route_timing(0, vehicle_info, road_lengths)
        assert route_timing == {"road1": [0, 1, 2, 3]}
