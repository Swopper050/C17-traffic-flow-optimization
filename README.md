# Optimizing Traffic Flow and Travel Time Using Multi-Agent Systems
## Group C17 - Design of Multi Agent System - University Of Groningen - Master of Science Artificial Intelligence

### Group Members:
 * Adithya M.S (s4214633)
 * Bram de Wit (s3151654)
 * Rik Vegter (s3147495)
 * Daniel Marouf (s4503619)

# About our Project

In this study, an approach using Multi-Agent Systems was used in order to optimize traffic flow and travel time. A new perspective is used in which agents implicitly communicate with each other by publishing their planned routes to a central agent. Agents can communicate with this central agent to foresee traffic jams and hence they will dynamically plan their route in order to minimize their own travel time. It is expected that this will also have a positive impact on the travel time, waiting time and the traffic congestion of all systems. OSMnx was used to simulate a part of the map of Manhattan, to make the simulation as realistic as possible. The results were compared to a baseline where all route planning was static.

# Packages

## [Folium](https://python-visualization.github.io/folium/index.html) - Map parser

"Folium builds on the data wrangling strengths of the Python ecosystem and the mapping strengths of the leaflet.js library. Manipulate your data in Python, then visualize it in on a Leaflet map via folium."

## [OSMNX](https://github.com/gboeing/osmnx) - Map libary

"Python for street networks
Retrieve, model, analyze, and visualize OpenStreetMap street networks and other spatial data.
Citation info: Boeing, G. 2017. "OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks." Computers, Environment and Urban Systems 65, 126-139. doi:10.1016/j.compenvurbsys.2017.05.004'"

## [Cityflow](https://cityflow-project.github.io/) - Simulation base

"CityFlow is a new designed open-source traffic simulator, which is much faster than SUMO (Simulation of Urban Mobility).

CityFlow can support flexible definitions for road network and traffic flow based on synthetic and real-world data. It also provides user-friendly interface for reinforcement learning. Most importantly, CityFlow is more than twenty times faster than SUMO and is capable of supporting city-wide traffic simulation with an interactive render for monitoring. Besides traffic signal control, CityFlow could serve as the base for other transportation studies and can create new possibilities to test machine learning methods in the intelligent transportation domain."
## [Astar](https://github.com/jrialland/python-astar) - A-* algorithm implementation

"This is a simple implementation of the a-star path finding algorithm in python."
## Other packages

* [Numpy](https://numpy.org/doc/stable/) - Multidimensional array
* [Matplotlib](https://matplotlib.org/3.3.2/contents.html) - Plot
* [Seaborn](https://seaborn.pydata.org/) - Statistical data visualization
* [Joblib](https://pypi.org/project/joblib/) - Lightweight pipelining
* [Sklearn](https://scikit-learn.org/stable/index.html) - predictive data analysis


# Installation
We recommend Docker because It works with all operating system Cityflow use C++ dependencies which not worked on Mac. Linux based OS could use both installations. 
## 1.  Docker

### [Docker Installation](https//docs.docker.com/engine/install/)
### Docker Build
Clone repository, build Docker: It takes around 10 minutes to build.
```
git clone https://github.com/Swopper050/C17-traffic-flow-optimization.git
cd C17-traffic-flow-optimization
docker build -t traffic_opt .
```
**Run the docker and cd to the directory:**
```
sudo docker run -dit --name traffic traffic_opt
sudo docker exec -i -t traffic bin/bash
cd /home/C17-traffic-flow-optimization/
```
## 2. Virtual environment

Clone repository. Install virtualenv, make virtual environment and install dependencies:
```
git clone https://github.com/Swopper050/C17-traffic-flow-optimization.git
cd C17-traffic-flow-optimization
pip3 install virtualenv
python3 -m venv .env
sudo apt -y install libspatialindex-c4v5 python3-pip
sudo apt install -y build-essential cmake
pip3 install -r requirements.txt
git clone https://github.com/cityflow-project/CityFlow.git 
cd CityFlow
pip3 install .
cd ..
```

# Running the simulation

### Default parameters:  
* map: low_monhattan  (Map Directory)
* Max Steps : 500 (Integer)
* Initial cars: 500 (Integer)
* New car / step : 1 (Integer)

### Printing the following statistics
* Average travel time 
* Free flow avg travel time 
* Average % waiting vehicles 
* Travel Time Index 
## Static
Simulation time: ~10 seconds
```
python3 run_static_routing_simulation.py --dir low_manhattan --max_steps 500 --cars_per_step 1 --init_cars 500
```
## Dynamic
Simulation time: ~50 seconds
```
python3 run_dynamic_routing_simulation.py --dir low_manhattan --max_steps 500 --cars_per_step 1 --init_cars 500

```
### Generated Replay files and plot for visualsation:
```
low_manhattan/replay.txt 
low_manhattan/replay_roadnet.json 
low_manhattan/waiting_vehicles.png .
```
**Copy the replay files and plot from the docker :**
```
docker create --name traffic_on traffic_opt
docker cp traffic_on:/home/C17-traffic-flow-optimization/low_manhattan/replay.txt .
docker cp traffic_on:/home/C17-traffic-flow-optimization/low_manhattan/replay_roadnet.json .
docker cp traffic_on:/home/C17-traffic-flow-optimization/low_manhattan/waiting_vehicles.png .
```

**Upload replay.txt and replay_roadnet.json here:**
[Show Simulation](http://108.61.178.181:6970/show) 

# From Virtual machine (only default parameters)
[Traffic flow optimization](http://108.61.178.181:6970/traffic_sim) - We made a webpage where the default dynamic and static simulation can be run.

# Results
* Steps (seconds): 500(~8 min), 1000(~17 min) and 1500(25 min)
* Numbers of initial cars: 500, 750 and 1000
* pawning rate: 1 car/step
* Numbers of simulations: 50  in each scenario

Simulation parameters|Travel time         |  Travel Time index | Waiting percent
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
500 steps, 500 cars|![](http://trinetti.co/dmas/boxplot_travel_500_500.png) | ![](http://trinetti.co/dmas/boxplot_tti_500_500.png) | ![](http://trinetti.co/dmas/boxplot_waiting_500_500.png)
500 steps, 750 cars|![](http://trinetti.co/dmas/boxplot_travel_500_750.png) |![](http://trinetti.co/dmas/boxplot_tti_500_750.png) |![](http://trinetti.co/dmas/boxplot_waiting_500_750.png) 
500 steps, 1000 cars|![](http://trinetti.co/dmas/boxplot_travel_500_1000.png) |![](http://trinetti.co/dmas/boxplot_tti_500_1000.png) |![](http://trinetti.co/dmas/boxplot_waiting_500_1000.png) 
1000 steps, 500 cars|![](http://trinetti.co/dmas/boxplot_travel_1000_500.png)|![](http://trinetti.co/dmas/boxplot_tti_1000_500.png) |![](http://trinetti.co/dmas/boxplot_waiting_1000_500.png) 
1000 steps, 750 cars|![](http://trinetti.co/dmas/boxplot_travel_1000_750.png)|![](http://trinetti.co/dmas/boxplot_tti_1000_750.png) |![](http://trinetti.co/dmas/boxplot_waiting_1000_750.png) 
1000 steps, 1000 cars|![](http://trinetti.co/dmas/boxplot_travel_1000_1000.png)|![](http://trinetti.co/dmas/boxplot_tti_1000_1000.png) |![](http://trinetti.co/dmas/boxplot_waiting_1000_1000.png) 
1500 steps, 500 cars|![](http://trinetti.co/dmas/boxplot_travel_1500_500.png)|![](http://trinetti.co/dmas/boxplot_tti_1500_500.png) |![](http://trinetti.co/dmas/boxplot_waiting_1500_500.png) 
1500 steps, 750 cars|![](http://trinetti.co/dmas/boxplot_travel_1500_750.png)|![](http://trinetti.co/dmas/boxplot_tti_1500_750.png) |![](http://trinetti.co/dmas/boxplot_waiting_1500_750.png) 
1500 steps, 1000 cars|![](http://trinetti.co/dmas/boxplot_waiting_1500_1000.png)|![](http://trinetti.co/dmas/boxplot_tti_1500_1000.png) |![](http://trinetti.co/dmas/boxplot_waiting_1500_1000.png) 

## Differences between static and Dynamic Routing
![alt text](http://trinetti.co/dmas/Simulation.PNG)
