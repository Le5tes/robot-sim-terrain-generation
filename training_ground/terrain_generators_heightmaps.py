import random
import numpy as np
import math

from training_ground.geom_utils import distance_from_line
from training_ground.types import Point

def noop(x,y):
    return 0

def choose_terrain(size, intensity, start, goal, scale = 1):
    try:
        if not type(start) is Point:
            start = Point(*start)
        
        if not type(goal) is Point:
            goal = Point(*goal)
    except:
        raise ValueError("start and goal should either be of type Point (from this module) or iterables of length 2")
        
    terrain_choice = jagged_terrain if intensity < 0.15 else random.choice((jagged_terrain,potholes_terrain,pillars_terrain,path_terrain))

    return terrain_choice(size,intensity,start,goal, scale)

def jagged_terrain(size, intensity, start, goal, scale = 1, permutation = noop):
    size = int(size/scale) + 1
    jaggedness = intensity

    permutation_field = np.array([
        [permutation(x * scale, y * scale) for y in range(size)] for x in range(size)
    ])

    heightmap = np.random.normal(size = (size,size), scale = jaggedness * scale) + permutation_field
    return heightmap

def potholes_terrain(size, intensity, start, goal, scale = 1):
    n = int(size / scale) + 1
    holes = set(item for tup in (
        ((x,y), (x-1, y), (x+1, y), (x, y-1), (x, y+1))
          for x in range(n) 
          for y in range(n) 
          if random.random() < 0.1 * intensity 
    ) for item in tup)



    def holes_permutation(x, y):
        return - (4 * ((x,y) in holes and not is_protected(x,y, start, goal))) + is_protected(x,y, start, goal)

    return jagged_terrain(size, intensity/2, start, goal, permutation = holes_permutation)

protected_radius = 1.3
def is_protected(x,y,start,goal):
    return np.linalg.norm(np.array((start.x - x, start.y-y))) < protected_radius or np.linalg.norm(np.array((goal.x - x, goal.y-y))) < protected_radius 

def pillars_terrain(size, intensity, start, goal, scale = 1 ):
    n = int(size / scale) + 1
    pillars = set(
        (x,y)
          for x in range(n) 
          for y in range(n) 
          if random.random() < 0.1 * intensity 
    )

    def pillars_permutation(x,y):
        return 10 * ((x,y) in pillars and not is_protected(x,y, start, goal)) + is_protected(x,y, start, goal)

    return jagged_terrain(size, intensity/2, start, goal, permutation = pillars_permutation)

def path_terrain(size, intensity, start, goal, scale = 1):
    print(size)
    path = [start]
    for _ in range(3):
        if random.random() < intensity * 0.8:
            path.append((random.random() * 20, random.random() * 20))
    path.append(goal)

    width = 2.2 - intensity

    def path_permutation(x,y):
        paths = zip(path[:-1], path[1:])
        point_in_path = any([distance_from_line(np.array(a),np.array(b),np.array([x,y])) < width for a, b in paths]) or \
        (x-start.x) ** 2 + (y-start.y)**2 < 0.5 or (x-goal.x) ** 2 + (y-goal.y)**2 < 0.5

        return - 12 * (not point_in_path)
    
    return jagged_terrain(size, intensity/2, start, goal, scale, permutation = path_permutation)