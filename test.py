from training_ground.terrain_generator import build_terrain, Point
from training_ground.build_world import terrain_types
import sys

if __name__ == "__main__":
    type = sys.argv[1] if len(sys.argv) == 2 and sys.argv[1] in terrain_types else 'jagged'

    build_terrain('./test', type, 20, 0.2, 'bob',  Point(0,-5), Point(0,5))
