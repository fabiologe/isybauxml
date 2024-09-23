from xml_parser import *
from typing import List, Dict, Set
from hydraulik.utils import num_potential_out

def build_graph(haltung_list: List) -> Dict[str, List[str]]:
    graph = {}
    for haltung in haltung_list:
        if haltung.ablauf not in graph:
            graph[haltung.ablauf] = []
        if haltung.zulauf not in graph:
            graph[haltung.zulauf] = []
        # Use a set to prevent duplicate connections
        if haltung.ablauf not in graph[haltung.zulauf]:
            graph[haltung.zulauf].append(haltung.ablauf)
    return graph

def dfs(graph: Dict[str, List[str]], node: str, visited: Set[str], path: List[str], routes: List[List[str]]):
    if node in visited:
        print(f"Cycle detected at node {node}. Path: {' -> '.join(path)}")
        return
    
    visited.add(node)
    path.append(node)
    
    # If no further connections, record the path
    if node not in graph or not graph[node]:
        routes.append(path.copy())
    else:
        for neighbor in graph[node]:
            dfs(graph, neighbor, visited, path, routes)
    
    path.pop()
    visited.remove(node)

def find_routes(outfalls: List, graph: Dict[str, List[str]]) -> Dict[str, List[List[str]]]:
    routes = {}
    for outfall in outfalls:
        outfall_name = outfall.objektbezeichnung
        routes[outfall_name] = []
        dfs(graph, outfall_name, set(), [], routes[outfall_name])
    return routes

def find_sewer_routes(schacht_list: List, haltung_list: List, bauwerk_list: List):
    # Include bauwerk_list in the outfall detection process
    outfalls = num_potential_out(schacht_list + bauwerk_list, haltung_list)
    
    # Build the graph including both haltung_list and bauwerk_list
    graph = build_graph(haltung_list)
   
    print("Graph Representation (zulauf -> ablauf):")
    for key, value in graph.items():
        print(f"{key} -> {value}")
 
    routes = find_routes(outfalls, graph)

    for outfall, paths in routes.items():
        print(f"Routes from outfall {outfall}:")
        for path in paths:
            print(" -> ".join(path))