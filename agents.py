# -*- coding: utf-8 -*-
"""
This file defines the agent class
"""
import json
import pdb
import os
from copy import copy


#flow_file_path                 -Sample flow file for reference
#agent_flow_file_path           -Flow file created based on simulation config

flow_file_path =  ".\\test_sim\\agents_flow.json"
agent_flow_file_path =  ".\\test_sim\\agents_flow.json"

#Class attributes are all derived from flow.json. Refer citiflow docs for description
class vehicle:
	vehicle_id = []

	def __init__(self, vehicle_prop):
		self.length = vehicle_prop.length
		self.width = vehicle_prop.length / 2.5       # Maintaining aspect ratio as 2.5
		self.maxPosAcc = vehicle_prop.maxPosAcc
		self.maxNegAcc = vehicle_prop.maxNegAcc
		self.usualPosAcc = vehicle_prop.maxPosAcc / 2.0  # Assuming usual acceleration is half of maximum acceleration
		self.usualNegAcc = vehicle_prop.maxNegAcc / 2.0
		self.minGap = vehicle_prop.minGap
		self.maxSpeed = vehicle_prop.maxSpeed
		self.headwayTime = vehicle_prop.headwayTime
		self.route = copy(vehicle_prop.route)
		self.interval = vehicle_prop.interval
		self.startTime = vehicle_prop.startTime
		self.endTime = vehicle_prop.endTime
		self.update_flow_json()

	def update_flow_json(self):
		if os.path.exists(agent_flow_file_path):
			with open(agent_flow_file_path) as f:
				flow_json = json.load(f)
		else:
			flow_json = []

		#Create a dict with class attributes and write to agents_flow.json

		new_entry = dict()
		new_entry['vehicle'] = dict()
		new_entry['vehicle']['length'] = self.length
		new_entry['vehicle']['width'] = self.width
		new_entry['vehicle']['maxPosAcc'] = self.maxPosAcc
		new_entry['vehicle']['maxNegAcc'] = self.maxNegAcc
		new_entry['vehicle']['usualPosAcc'] = self.usualPosAcc
		new_entry['vehicle']['usualNegAcc'] = self.usualNegAcc
		new_entry['vehicle']['minGap'] = self.minGap
		new_entry['vehicle']['maxSpeed'] = self.maxSpeed
		new_entry['vehicle']['headwayTime'] = self.headwayTime
		new_entry['route'] = copy(self.route)
		new_entry['interval'] = self.interval
		new_entry['startTime'] = self.startTime
		new_entry['endTime'] = self.endTime

		if new_entry not in flow_json:
			flow_json.append(new_entry)
		else:
			print("Similar entry already present")

		with open(agent_flow_file_path, 'w+') as f:
			json.dump(flow_json,f)

		return
