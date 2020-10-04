import json
import random


def generate_random_flow_file(*, n_steps, cars_per_step=1):
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

    agent_configs = []
    for step in range(n_steps):
        for i in range(cars_per_step):
            random_indices = random.sample(range(0, len(roadnet_json["roads"]) - 1), 2)
            car_config = {
                "vehicle": {
                    "length": 5,
                    "width": 2,
                    "maxPosAcc": 2.0,
                    "maxNegAcc": 4.5,
                    "usualPosAcc": 2.0,
                    "usualNegAcc": 4.5,
                    "minGap": 2.5,
                    "maxSpeed": 200,
                    "headwayTime": round(random.uniform(1, 3), 1),
                },
                "route": [
                    roadnet_json["roads"][index]["id"] for index in random_indices
                ],
                "interval": 100,
                "startTime": step,
                "endTime": step + 10,
            }
            agent_configs.append(car_config)

    with open("./low_manhattan_sim/low_manhattan_flow.json", "w") as f:
        json.dump(agent_configs, f)
