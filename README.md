# Design of Multi-Agent Systems project 2020
# Optimizing Traffic Flow and Travel Time Using Multi-Agent Systems 
Group C17
 - Rik
 - Adithya
 - Bram
 - Daniel
# Simulate traffic on virtual machine 
http://108.61.178.181:6969/traffic_sim

# Setup on local computer
Clone repository. Install virtualenv, make virtual environment and install dependencies:
```
git clone https://github.com/Swopper050/C17-traffic-flow-optimization.git
cd dmas2020
pip install virtualenv
python -m venv .env
pip install -r requirements.txt
sudo apt update && sudo apt install -y build-essential cmake
git clone https://github.com/cityflow-project/CityFlow.git 
pip install .
```
# Configuration
Default Simulation:  
map: low_monhattan (converted from osmnx)  
max_steps : 10  
busy_road_thereshold : 4  
```
python test_make_sim.py
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
