import random
import numpy as np

def jagged_terrain(size, intensity):
    jaggedness = intensity

    heightmap = np.random.normal(size = (size,size), scale = jaggedness)

    plane_vertices = np.array([
        [x,y, heightmap[x,y]]
        for x in range(size)
        for y in range(size)
    ])

    plane_faces = np.array([
        [x, x+size, x+1] 
        for x in range(size * (size - 1))
        if x % size != size - 1
    ] + [
        [x+1, x+size, x+size+1] 
        for x in range(size * (size - 1))
        if x % size != size - 1
    ])

    return plane_vertices, plane_faces

def boxes_terrain(size, intensity):
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

    plane_vertices = np.array([vertex for row in boxes for box in row for vertex in box]) # just flatten boxes to get the vertices

    plane_faces = np.array(
        face 
        for item in(
            # box tops
            [
                [
                    [box[0], box[1], box[2]], 
                    [box[1], box[2], box[3]]
                ] for row in boxes for box in row
            ] + 
            # box sides (just 2 sides)
            [
                [
                    [boxes[y][x][1], boxes[y][x][3], boxes[y][x+1][2]],
                    [boxes[y][x][1], boxes[y][x+1][0], boxes[y][x+1][2]],
                    [boxes[y][x][2], boxes[y][x][3], boxes[y+1][x][0]],
                    [boxes[y][x][3], boxes[y+1][x][0], boxes[y+1][x][1]],
                ] for x in range(size - 1) for y in range(size - 1)
            ]
        ) 
        for face in item
        )

    return plane_vertices, plane_faces

def stairs_terrain(size, intensity):
    x_direction = random.randint(-1,1)
    y_direction = random.randint(-1,1)
    while x_direction == 0 and y_direction == 0:
        x_direction = random.randint(-1,1)
        y_direction = random.randint(-1,1)
    x_vertices = [
       [[x,y] for x in range(size//2 - (size*x_direction)//2, size//2 + (size*x_direction)//2 + x_direction, x_direction) ] 
       for y in [size/2 - size*(y_direction or 1)/2, size/2 + size*(y_direction or 1)/2]  
    ] if x_direction != 0 else [[],[]]
    y_vertices = [
       [[x,y] for y in range(size//2 - (size*y_direction)//2, size//2 + (size*y_direction)//2 + y_direction, y_direction) ] 
       for x in [size/2 - size*(x_direction or 1)/2, size/2 + size*(x_direction or 1)/2]  
    ] if y_direction != 0 else [[],[]]

    def get_stair(stair, i, length, intensity):
        out = [
            stair[0][0],stair[0][1][-i * intensity],
            stair[1][0],stair[1][1][-i * intensity],
            stair[0][0],stair[0][1][-(i+1) * intensity],
            stair[1][0],stair[1][1][-(i+1) * intensity],
        ]
        if i == 0:
            out = out[2:]
        elif i == length:
            out = out[:2]
        if len(out == 2) and out[0] == out[1]:
            out = out[:1]
        return out

    stair_locations = list(dict.fromkeys(list(zip(x_vertices[0] + y_vertices[1], y_vertices[0] + x_vertices[1]))))

    stairs =  [get_stair(stair, i, len(stair_locations, intensity)) for stair in stair_locations]

    stairs[0].pop

    plain_vertices = np.array([vertex for stair in stairs for vertex in stair])
    plain_faces = np.array(zip(
        plain_vertices[:-2],
        plain_vertices[1:-1],
        plain_vertices[2:]
    ))

    return plain_vertices, plain_faces
