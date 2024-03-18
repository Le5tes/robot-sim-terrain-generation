import random
import numpy as np
import math

from training_ground.geom_utils import distance_from_line

def noop(x,y):
    return 0

def jagged_terrain(size, intensity, start, goal, scale = 1, permutation = noop):
    size = int(size/scale) + 1
    jaggedness = intensity
    print(size)

    permutation_field = np.array([
        [permutation(x * scale, y * scale) for y in range(size)] for x in range(size)
    ])
    print(permutation_field.shape)

    heightmap = np.random.normal(size = (size,size), scale = jaggedness * scale) + permutation_field
    print(heightmap.shape)
    return heightmap

def potholes_terrain(size, intensity, start, goal, scale = 1):
    n = int(size / scale) + 1
    holes = set(item for tup in (
        ((x,y), (x-1, y), (x+1, y), (x, y-1), (x, y+1))
          for x in range(n) 
          for y in range(n) 
          if random.random() < 0.1 * intensity 
    ) for item in tup)

    startSet = set(((start.x, start.y), (start.x+1, start.y), (start.x, start.y+1), (start.x-1, start.y), (start.x, start.y-1)))

    goalSet = set(((goal.x, goal.y), (goal.x+1, goal.y), (goal.x, goal.y+1), (goal.x-1, goal.y), (goal.x, goal.y-1)))

    protected = startSet | goalSet


    def holes_permutation(x, y):
        return - (4 * ((x,y) in holes and (x,y) not in protected))

    return jagged_terrain(size, intensity/2, start, goal, permutation = holes_permutation)

def pillars_terrain(size, intensity, start, goal, scale = 1 ):
    n = int(size / scale) + 1
    pillars = set(
        (x,y)
          for x in range(n) 
          for y in range(n) 
          if random.random() < 0.1 * intensity 
    )

    startSet = set(((start.x, start.y), (start.x+1, start.y), (start.x, start.y+1), (start.x-1, start.y), (start.x, start.y-1)))

    goalSet = set(((goal.x, goal.y), (goal.x+1, goal.y), (goal.x, goal.y+1), (goal.x-1, goal.y), (goal.x, goal.y-1)))

    protected = startSet | goalSet

    def pillars_permutation(x,y):
        return 10 * ((x,y) in pillars and (x,y) not in protected)

    return jagged_terrain(size, intensity/2, start, goal, permutation = pillars_permutation)

def path_terrain(size, intensity, start, goal, scale = 1):
    print(size)
    path = [start]
    for _ in range(3):
        if random.random() < intensity * 0.8:
            path.append((random.random() * 20, random.random() * 20))
    path.append(goal)

    width = 1.1 - intensity

    def path_permutation(x,y):
        paths = zip(path[:-1], path[1:])
        point_in_path = any([distance_from_line(np.array(a),np.array(b),np.array([x,y])) < width for a, b in paths]) or \
        (x-start.x) ** 2 + (y-start.y)**2 < 0.5 or (x-goal.x) ** 2 + (y-goal.y)**2 < 0.5

        return - 12 * (not point_in_path)
    
    return jagged_terrain(size, intensity/2, start, goal, scale, permutation = path_permutation)