import numpy as np
def cube(size):    
    bottom_z = -size/2
    top_z = size/2
    box_vertices = np.array([
        (0,0,top_z),
        (0,size, top_z),
        (size, 0, top_z),
        (size, size, top_z),
        (0,0,bottom_z),
        (0,size, bottom_z),
        (size, 0, bottom_z),
        (size, size, bottom_z),
    ])

    box_faces = np.array([
        (2,1,0),
        (2,3,1),
        (1,4,0),
        (1,5,4),
        (3,5,1),
        (3,7,5),
        (0,6,2),
        (0,4,6),
        (2,7,3),
        (2,6,7),
        (5,6,4),
        (7,6,5)
    ])

    return box_vertices, box_faces