import random
import numpy as np

def noop(height, x,y):
    return height

def jagged_terrain(size, intensity, start, goal, scale = 1, permutation = noop):
    size = int(size/scale)
    jaggedness = intensity

    heightmap = np.random.normal(size = (size,size), scale = jaggedness * scale)

    plane_vertices = np.array([
        [x * scale,y * scale, permutation(heightmap[x,y], x * scale, y * scale)]
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

def potholes_terrain(size, intensity, start, goal):
    holes = set(item for tup in (
        ((x,y), (x-1, y), (x+1, y), (x, y-1), (x, y+1))
          for x in range(size) 
          for y in range(size) 
          if random.random() < 0.1 * intensity 
    ) for item in tup)

    startSet = set(((start.x, start.y), (start.x+1, start.y), (start.x, start.y+1), (start.x-1, start.y), (start.x, start.y-1)))

    goalSet = set(((goal.x, goal.y), (goal.x+1, goal.y), (goal.x, goal.y+1), (goal.x-1, goal.y), (goal.x, goal.y-1)))

    protected = startSet | goalSet


    def holes_permutation(z, x, y):
        return z - (4 * ((x,y) in holes and (x,y) not in protected))

    return jagged_terrain(size, intensity/2, start, goal, permutation = holes_permutation)

def pillars_terrain(size, intensity, start, goal):

    pillars = set(
        (x,y)
          for x in range(size) 
          for y in range(size) 
          if random.random() < 0.1 * intensity 
    )

    startSet = set(((start.x, start.y), (start.x+1, start.y), (start.x, start.y+1), (start.x-1, start.y), (start.x, start.y-1)))

    goalSet = set(((goal.x, goal.y), (goal.x+1, goal.y), (goal.x, goal.y+1), (goal.x-1, goal.y), (goal.x, goal.y-1)))

    protected = startSet | goalSet

    def pillars_permutation(z,x,y):
        return z + (10 * ((x,y) in pillars and (x,y) not in protected))

    return jagged_terrain(size, intensity/2, start, goal, permutation = pillars_permutation)


def distance_from_line(a,b,p):
    line_length = np.linalg.norm(b-a)
    unit_vector = (b-a)/line_length

    if np.dot(p, unit_vector) < np.dot(a, unit_vector):
        return np.linalg.norm(a-p)
    elif np.dot(p, unit_vector) > np.dot(b, unit_vector):
        return np.linalg.norm(b-p)
    else:
        projection_to_ab = (a-p) + np.dot(p - a, unit_vector) * unit_vector
        return np.linalg.norm(projection_to_ab)

def path_terrain(size, intensity, start, goal):
    path = [start]
    for _ in range(3):
        if random.random() < intensity * 0.8:
            path.append((random.random() * 20, random.random() * 20))
    path.append(goal)

    width = 1.1 - intensity

    def path_permutation(z,x,y):
        paths = zip(path[:-1], path[1:])
        point_in_path = any([distance_from_line(np.array(a),np.array(b),np.array([x,y])) < width for a, b in paths]) or \
        (x-start.x) ** 2 + (y-start.y)**2 < 0.5 or (x-goal.x) ** 2 + (y-goal.y)**2 < 0.5

        return z - 10 * (not point_in_path)
    
    return jagged_terrain(size, intensity/2, start, goal, scale = 0.2, permutation = path_permutation)
