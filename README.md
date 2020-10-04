# Optimizing Traffic Flow and Travel Time Using Multi-Agent Systems 
Group C17
 - Rik
 - Adithya
 - Bram
 - Daniel
# Simulate traffic on virtual machine 
http://108.61.178.181:6969/traffic_sim
# Docker Installation
https://docs.docker.com/engine/install/
# Setup on local computer by Docker
Clone repository, build Docker:
```
git clone https://github.com/Swopper050/C17-traffic-flow-optimization.git
cd C17-traffic-flow-optimization
docker build -t tarffic_opt .
```
Copy the replay files for visualisation from the docker:
```
docker create --name traffic_on traffic_opt
docker cp traffic_on:/home/C17-traffic-flow-optimization/low_manhattan_sim/replay.txt .
docker cp traffic_on:/home/C17-traffic-flow-optimization/low_manhattan_sim/replay_roadnet.json .
```
Upload replay files here:
http://108.61.178.181:6969/show
Or /fronted/index.html
```
sudo docker run -dit --name traffic traffic_opt
sudo docker exec -i -t traffic bin/bash
cd /home/C17-traffic-flow-optimization/
```
# Configuration
Default Simulation:  
map: low_monhattan  
max_steps : 500 
Run simulation 
```
python run_static_routing_simulation.py
```
Config files
```
low_manhattan_sim/config.json
low_manhattan_sim/agents_flow.json
low_manhattan_sim/low_manhattan.json
low_manhattan_sim/low_manhattan_flow.json
```
