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

G = ox.graph_from_point((40.78343, -73.96625), dist=1000, network_type="drive")
# G = ox.graph_from_place("New York City, New York", network_type="drive")
import pdb; pdb.set_trace()
