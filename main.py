import pdb
import osmnx as ox

from utils import get_traffic_light_nodes

G = ox.graph_from_place("Groningen, Netherlands", network_type="drive")
traffic_nodes = get_traffic_light_nodes(G)
pdb.set_trace()
