import json
import random


def generate_random_flow_file(*, n_steps, cars_per_step=1, n_init_cars=100):
    """
    This function generates a flow file to be used by CityFlow. It generates a specified
    number of cars every step. Every individual car is considered an Agent, and all agents
    are eventually written to the flow file: low_manhattan_flow.json

    :param n_steps: number of steps in the simulation
    :param cars_per_step: number of cars to spawn every simulation step
    """

    with open("./low_manhattan_sim/low_manhattan.json") as f:
        roadnet_json = json.load(f)
    road_indices = []

    agent_configs = [generate_random_car_config(roadnet_json, 0) for _ in range(n_init_cars)]
    for step in range(n_steps):
        for i in range(cars_per_step):
            agent_configs.append(generate_random_car_config(roadnet_json, step))

    with open("./low_manhattan_sim/low_manhattan_flow.json", "w") as f:
        json.dump(agent_configs, f, indent=4)


def generate_random_car_config(roadnet_json, spawn_time):
    """ Generates a random configuration for spawning a single car.

    :param roadnet_json: json file describing the roadnet
    :param spawn_time: step/time at which to spawn the car
    :returns: dictionary in json format with car characteristics
    """

    random_indices = random.sample(range(0, len(roadnet_json["roads"]) - 1), 2)
    return {
        "vehicle": {
            "length": 5,
            "width": 2,  # Maintaining aspect ratio as 2.5
            "maxPosAcc": random.uniform(1, 4),
            "maxNegAcc": random.uniform(3, 6),
            "usualPosAcc": 1.0,
            "usualNegAcc": 2.5,
            "minGap": 2.5,
            "maxSpeed": 10,
            "headwayTime": round(random.uniform(1, 3), 1),
        },
        "route": [
            roadnet_json["roads"][index]["id"] for index in random_indices
        ],
        "interval": 100,
        "startTime": spawn_time,
        "endTime": spawn_time + 10,
    }
