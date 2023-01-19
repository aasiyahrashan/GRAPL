# -*- coding: utf-8 -*-

# Adapted from https://helenedk.medium.com/implementing-the-d-separation-algorithm-in-python-886ef1979759

def dsep(startNodes, endNodes, givenNodes, G):

    L = {givenNodes}.copy()
    ancestors = []

    while L:

        tempNode = L.pop()

        if not tempNode in ancestors:
            parent = G.pa(tempNode)
            L = L.update(parent)

        ancestors = ancestors + list(tempNode)

    ancestors = list(dict.fromkeys((ancestors)))

    L = [(startNodes, True)]
    Reachable, Visited = [], []

    while len(L) > 0:

        tempNode, up = L.pop()

        if not (tempNode, up) in Visited:
            Reachable = Reachable + [tempNode] if tempNode not in givenNodes else []
            Visited = Visited + [(tempNode, up)]

            if (not tempNode in givenNodes) & up:
                L = L + [(v, True) for v in G.pa(tempNode)] + [(v, False) for v in G.ch(tempNode)]

            if not up:
                if not tempNode in givenNodes: L = L + [(v, False) for v in G.ch(tempNode)]
                if tempNode in ancestors: L = L + [(v, True) for v in G.pa(tempNode)]

    reachable_nodes = list(dict.fromkeys(Reachable))

    if type(endNodes) != list:
        endNode_temp = []
        endNode_temp.append(endNodes)
    elif type(endNodes) == list:
        endNode_temp = endNodes

    answer = all(i in reachable_nodes for i in endNode_temp)

    if answer == True:
        answer = "Not d-separated"
    else:
        answer = "d-separated"

    return(answer)