import sys
from main import main
from glob import glob
from map_generator import map_nodes, MAP_DIRECTORY
from os import path
import json
import os

class MapStatifier:
    def __init__(self, argv):
        if not os.path.exists('/home/dev/PycharmProjects/AStarHeuristic/maps'):
            os.makedirs('/home/dev/PycharmProjects/AStarHeuristic/maps')

        map_nodes()
        all_results = {}
        for map_file in glob(path.join(MAP_DIRECTORY, "*")):
            print("working on..." + map_file)
            all_results[path.basename(map_file)] = main(argv, map_file)

        avg_results = {
            "time": 0.0,
            "cost": 0.0,
            "nodes_expanded": 0.0,
            "count": 0,
            "path_length": 0.0,
        }

        for res in all_results.values():
            if res.get("time") != -1:
                avg_results['count'] += 1
                avg_results['time'] += res.get('time')
                avg_results['cost'] += res.get('cost')
                avg_results['nodes_expanded'] += res.get('nodes_expanded')
                avg_results['path_length'] += res.get('path_length')

        avg_results['time'] /= avg_results['count']
        avg_results['cost'] /= avg_results['count']
        avg_results['nodes_expanded'] /= avg_results['count']
        avg_results['path_length'] /= avg_results['path_length']

        with open("results.json", "w") as f:
            f.write(json.dumps(dict(maps=all_results, average=avg_results), indent=4))


if __name__ == "__main__":
    m = MapStatifier(sys.argv[:])
    # m = MapStatifier((None, '5', '1'))