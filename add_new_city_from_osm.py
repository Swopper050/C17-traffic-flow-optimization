"""
Skeleton script used to convert OSM maps to a format usable by CityFlow
"""

import osmnx as ox


53.217293, 6.566559  # Groningen
40.743382, -73.988689  # low manhattan
40.701318, -73.927438  # brooklyn



if __name__ == "__main__":
    utn = ox.settings.useful_tags_node
    oxna = ox.settings.osm_xml_node_attrs
    oxnt = ox.settings.osm_xml_node_tags
    utw = ox.settings.useful_tags_way
    oxwa = ox.settings.osm_xml_way_attrs
    oxwt = ox.settings.osm_xml_way_tags
    utn = list(set(utn + oxna + oxnt))
    utw = list(set(utw + oxwa + oxwt))
    ox.config(all_oneway=True, useful_tags_node=utn, useful_tags_way=utw)

    G = ox.graph_from_address('Gedempte Zuiderdiep 95, Groningen, Netherlands', network_type="drive")
    # G = ox.graph_from_place("New York City, New York", network_type="drive")

    # ox.plot_graph(G)

    ox.save_graph_xml(G, "test_graph.osm")
