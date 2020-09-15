import osmnx as ox

utn = ox.settings.useful_tags_node
oxna = ox.settings.osm_xml_node_attrs
oxnt = ox.settings.osm_xml_node_tags
utw = ox.settings.useful_tags_way
oxwa = ox.settings.osm_xml_way_attrs
oxwt = ox.settings.osm_xml_way_tags
utn = list(set(utn + oxna + oxnt))
utw = list(set(utw + oxwa + oxwt))
ox.config(all_oneway=True, useful_tags_node=utn, useful_tags_way=utw)

G = ox.graph_from_point((53.217293, 6.566559), dist=1200, network_type="drive")
# G = ox.graph_from_place("New York City, New York", network_type="drive")
ox.plot_graph(G)
import pdb; pdb.set_trace()

53.217293, 6.566559  # Groningen
40.743382, -73.988689  # low manhattan
40.701318, -73.927438  # brooklyn
