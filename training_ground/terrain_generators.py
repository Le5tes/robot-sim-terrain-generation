import random
import numpy as np
import math
from training_ground.box import cube
import training_ground.terrain_generators_heightmaps as hm
from training_ground.cylinder import create_cylinder
from training_ground.geom_utils import distance_from_line
from training_ground.shape_utils import combine_shapes, invert_shape_faces

def noop(height, x,y):
    return height

def with_bounding_box(terrain, size):
    bounding_box = invert_shape_faces(cube(size))
    return combine_shapes(terrain, bounding_box)

def from_heightmap(heightmap, size, scale):
    n = int(size/scale) + 1
    plane_vertices = np.array([
        [x * scale,y * scale, heightmap[x,y]]
        for x in range(n)
        for y in range(n)
    ])

    plane_faces = np.array([
        [x, x+n, x+1] 
        for x in range(n * (n - 1))
        if x % n != n - 1
    ] + [
        [x+1, x+n, x+n+1] 
        for x in range(n * (n - 1))
        if x % n != n - 1
    ])

    return plane_vertices, plane_faces

def jagged_terrain(size, intensity, start, goal, scale = 1, permutation = noop):
    heightmap = hm.jagged_terrain(size, intensity, start, goal, scale)

    return from_heightmap(heightmap, size, scale)

def boxes_terrain(size, intensity, start, goal):
    heightmap = np.random.normal(size = (size,size), scale = intensity)

    # maintain a 2d structure of boxes for readability
    boxes = [
        [
            [
                [x,y, heightmap[x,y]],
                [x+1,y, heightmap[x,y]],
                [x,y+1, heightmap[x,y]],
                [x+1,y+1, heightmap[x,y]]
            ]
            for x in range(size)
        ]
        for y in range(size)
    ]

    plane_vertices = [vertex for row in boxes for box in row for vertex in box] # just flatten boxes to get the vertices

    def v_index(point):
        return plane_vertices.index(point)

    box_faces_nested = [
                [ # box tops
                    [v_index(box[0]), v_index(box[1]), v_index(box[2])], 
                    [v_index(box[2]), v_index(box[1]), v_index(box[3])]
                ] for row in boxes for box in row
            ] + [
                [ # box sides (just 2 sides)
                    [v_index(boxes[y][x][3]), v_index(boxes[y][x][1]), v_index(boxes[y][x+1][2])],
                    [v_index(boxes[y][x][1]), v_index(boxes[y][x+1][0]), v_index(boxes[y][x+1][2])],
                    [v_index(boxes[y][x][2]), v_index(boxes[y][x][3]), v_index(boxes[y+1][x][0])],
                    [v_index(boxes[y+1][x][0]), v_index(boxes[y][x][3]), v_index(boxes[y+1][x][1])],
                ] for x in range(size - 1) for y in range(size - 1)
            ]


    plane_faces = np.array(tuple(
        face 
        for item in box_faces_nested
        for face in item
    ))


    return np.array(plane_vertices), plane_faces

def stairs_terrain(size, intensity, start, goal):
    x_direction = random.randint(-1,1)
    y_direction = random.randint(-1,1)

    while x_direction == 0 and y_direction == 0:
        x_direction = random.randint(-1,1)
        y_direction = random.randint(-1,1)
    x_vertices = [
       [(x,y) for x in range(size//2 - (size*x_direction)//2, size//2 + (size*x_direction)//2 + x_direction, x_direction) ] 
       for y in [size/2 - size*(y_direction or 1)/2, size/2 + size*(y_direction or 1)/2]  
    ] if x_direction != 0 else [[],[]]
    y_vertices = [
       [(x,y) for y in range(size//2 - (size*y_direction)//2, size//2 + (size*y_direction)//2 + y_direction, y_direction) ] 
       for x in [size/2 - size*(x_direction or 1)/2, size/2 + size*(x_direction or 1)/2]  
    ] if y_direction != 0 else [[],[]]

    def get_stair(stair, i, length, intensity):
        out = [
            [stair[0][0],stair[0][1],-i * intensity],
            [stair[1][0],stair[1][1],-i * intensity],
            [stair[0][0],stair[0][1],-(i+1) * intensity],
            [stair[1][0],stair[1][1],-(i+1) * intensity],
        ]
        if i == 0:
            out = out[2:]
        elif i == length:
            out = out[:2]
        if len(out) == 2 and out[0] == out[1]:
            out = out[:1]
        return out

    stair_locations = list(dict.fromkeys(list(zip(x_vertices[0] + y_vertices[1], y_vertices[0] + x_vertices[1]))))

    stairs =  [get_stair(stair, i, len(stair_locations), intensity) for i, stair in enumerate(stair_locations)]

    stairs[0].pop

    plain_vertices = np.array([vertex for stair in stairs for vertex in stair])

    v_indices =range(len(plain_vertices))

    # TODO: This is really terrible code. Make it more intuitive.
    plain_faces = np.array(tuple(face if i % 2 == int(sum((x_direction, y_direction)) in [0,1]) else tuple(reversed(face)) for i, face in enumerate(zip(
        v_indices[:-2],
        v_indices[1:-1],
        v_indices[2:]
    ))))

    return plain_vertices, plain_faces

def potholes_terrain(size, intensity, start, goal, scale = 1):
    heightmap = hm.potholes_terrain(size, intensity, start, goal, scale)

    return from_heightmap(heightmap, size, scale)

def pillars_terrain(size, intensity, start, goal, scale = 1):
    heightmap = hm.pillars_terrain(size, intensity, start, goal, scale)

    return from_heightmap(heightmap, size, scale)

def path_terrain(size, intensity, start, goal, scale = 0.2):
    heightmap = hm.path_terrain(size, intensity, start, goal, scale)

    return from_heightmap(heightmap, size, scale)

def poles_terrain(size, intensity, start, goal):
    ground = jagged_terrain(size, intensity/2, start, goal, scale = 0.5)

    number_of_poles = random.randint(50 * intensity, 100 * intensity)

    def pole_intersects_start_or_end(pole_start, pole_end):
        return distance_from_line(pole_start[:2], pole_end[:2], start) < 1.5 or distance_from_line(pole_start[:2], pole_end[:2], goal) < 1.5

    poles = []

    for _ in range(number_of_poles):
        intersects = True
        pole_start = None
        pole_end = None
        while intersects:
            def random_point():
                return np.array([random.random() * size, random.random() * size, random.random() * 10 -3])
            pole_start = random_point()
            pole_end = random_point()
            intersects = pole_intersects_start_or_end(pole_start, pole_end)
        print(pole_start, pole_end, np.linalg.norm(pole_end - pole_start))
        poles.append(create_cylinder(random.random() * 0.3, pole_start, pole_end, 6))

    # poles = [create_cylinder(0.5,np.array([0,0,0]), np.array([1,1,1]), 6)]
    # return poles[0]
    return combine_shapes(ground, *poles)