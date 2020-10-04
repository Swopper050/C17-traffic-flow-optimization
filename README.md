# Design of Multi-Agent Systems project 2020
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
sudo docker build -t tarfficopt .
sudo docker run -dit --name traffic trafficopt
sudo docker exec -i -t traffic
```
Inside the docker:
```
cd /home/C17-traffic-flow-optimization/
```
# Configuration
Default Simulation:  
map: low_monhattan (converted from osmnx)  
max_steps : 500  
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
# Results
Open frontend/index.html  
Upload replay_roadnet.json and replay.txt  
Start simulation  
