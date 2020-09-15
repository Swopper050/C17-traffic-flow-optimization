# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 20:55:54 2020

@author: 91782
"""
import json
import pdb
import os

flow_file_path =  ".\\test_sim\\flow.json"
agent_flow_file_path =  ".\\test_sim\\agents_flow.json"
class vehicle:
    vehicle_id = []
    
    def __init__(self, vehicle_prop):
        self.length = vehicle_prop.length
        self.width = vehicle_prop.width
        self.maxPosAcc = vehicle_prop.maxPosAcc
        self.maxNegAcc = vehicle_prop.maxNegAcc
        self.usualPosAcc = vehicle_prop.usualPosAcc
        self.usualNegAcc = vehicle_prop.usualNegAcc
        self.minGap = vehicle_prop.minGap
        self.maxSpeed = vehicle_prop.maxSpeed
        self.headwayTime = vehicle_prop.headwayTime
        self.route = vehicle_prop.route
        self.interval = vehicle_prop.interval
        self.startTime = vehicle_prop.startTime
        self.endTime = vehicle_prop.endTime
		
def update_flow_json():
	pdb.set_trace()
	if os.path.exists(agent_flow_file_path):
		with open(agent_flow_file_path) as f:
			flow_json = json.load(f)
	else:
		if os.path.exists(flow_file_path):
			with open(flow_file_path) as f:
				flow_json = json.load(f)
			with open(agent_flow_file_path, 'w') as f:
				json.dump(flow_json,f)
		else:
			raise Exception("Default flow file not found")
	#with open(agent_flow_file_path) as f:
			