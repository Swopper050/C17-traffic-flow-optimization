from types import SimpleNamespace

import pytest

from central_system import CentralSystem


class TestDynamicRoutePlanner:
    @pytest.fixture
    def config(self):
        return SimpleNamespace(
            dir="low_manhattan",
            max_steps=10,
            cars_per_step=1,
            init_cars=100,
        )

    @pytest.fixture
    def central_system(self, config):
        cs = CentralSystem(config)
        cs.map_density_over_time = {
            "road1": [[] for _ in range(cs.config.max_steps)],
            "road2": [[] for _ in range(cs.config.max_steps)],
            "road3": [[] for _ in range(cs.config.max_steps)],
            "road4": [[] for _ in range(cs.config.max_steps)],
            "road5": [[] for _ in range(cs.config.max_steps)],
        }
        return cs

    def test_init(self, config):
        cs = CentralSystem(config)
        assert cs.config is not None
        assert cs.map_density_over_time == {}

    def test_add_route(self, central_system):
        route_dict = {
            "road1": [0, 1, 2],
            "road2": [3, 4],
            "road4": [5, 6, 7, 8],
        }

        central_system.add_route("car1", route_dict)

        assert central_system.map_density_over_time == {
            "road1": [["car1"], ["car1"], ["car1"], [], [], [], [], [], [], []],
            "road2": [[], [], [], ["car1"], ["car1"], [], [], [], [], []],
            "road3": [[], [], [], [], [], [], [], [], [], []],
            "road4": [[], [], [], [], [], ["car1"], ["car1"], ["car1"], ["car1"], []],
            "road5": [[], [], [], [], [], [], [], [], [], []],
        }

    def test_remove_route(self, central_system):
        central_system.map_density_over_time = {
            "road1": [["car1"], ["car1"], ["car1"], [], [], [], [], [], [], []],
            "road2": [[], [], [], ["car1"], ["car1"], [], [], [], [], []],
            "road3": [[], [], [], [], [], [], [], [], [], []],
            "road4": [[], [], [], [], [], ["car1"], ["car1"], ["car1"], ["car1"], []],
            "road5": [[], [], [], [], [], [], [], [], [], []],
        }

        route_dict = {
            "road1": [0, 1, 2],
            "road2": [3, 4],
            "road4": [5, 6, 7, 8],
        }

        central_system.remove_route("car1", route_dict)

        assert central_system.map_density_over_time == {
            "road1": [[], [], [], [], [], [], [], [], [], []],
            "road2": [[], [], [], [], [], [], [], [], [], []],
            "road3": [[], [], [], [], [], [], [], [], [], []],
            "road4": [[], [], [], [], [], [], [], [], [], []],
            "road5": [[], [], [], [], [], [], [], [], [], []],
        }

    def test_remove_route_not_found(self, central_system):
        central_system.map_density_over_time = {
            "road1": [["car1"], ["car1"], ["car1"], [], [], [], [], [], [], []],
        }
        central_system.remove_route("car2", {"road1": [1, 2, 3]})  # Wrong car_id

        # Make sure the car is not removed
        assert central_system.map_density_over_time == {
            "road1": [["car1"], ["car1"], ["car1"], [], [], [], [], [], [], []],
        }

    def test_get_density_at_interval(self, central_system):
        central_system.map_density_over_time = {
            "road1": [["car1"], ["car1"], ["car1"], [], [], [], [], [], [], []],
            "road2": [[], [], [], ["car1"], ["car1"], [], [], [], [], []],
            "road3": [[], [], [], [], [], [], [], [], [], []],
            "road4": [
                [],
                [],
                [],
                [],
                [],
                ["car1"],
                ["car1"],
                ["car1", "car2"],
                ["car1"],
                [],
            ],
            "road5": [[], [], [], [], [], [], [], [], [], []],
        }

        density = central_system.get_density_at_interval("road4", 5, 10)

        assert density == {
            5: 1,
            6: 1,
            7: 2,
            8: 1,
            9: 0,
        }
