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

