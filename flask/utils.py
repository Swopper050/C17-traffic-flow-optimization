def get_traffic_light_nodes(G):
    """
    Given a graph (as loaded with osmnx), returns all nodes with traffic lights. This is done
    using the degrees of the graph. If the degree is higher than 3, it is considered a traffic
    light node.

    :param G: Graph instance
    :returns: list of traffic light nodes
    """

    return [node for node in G.degree() if node[1] > 3]

def filterDicForZero(dic):
    newDic = dict()
    for key, value in dic.items():
        if value > 0:
            newDic[key] = value
    return newDic
