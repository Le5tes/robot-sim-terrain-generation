import numpy as np
import math
## Rotates a point cloud so that the z axis is oriented along the input vector
def rotate_to_follow_vector(vector, vertices):
    ## calculate difference in angle between z axis and vector projected onto xz plane
    # print(vertices)
    # xz_vector = vector.dot(np.array([
    #     [1,0,0],
    #     [0,0,0],
    #     [0,0,1]
    # ]))
    ry_angle = (-1 if vector[0] > 0 else 1) * math.acos(vector[2]/np.linalg.norm(vector))
    # if vector[1] < 0:
    #     ry_angle += math.pi
    # print(ry_angle)

    ry = np.array([
        [math.cos(ry_angle), 0, -math.sin(ry_angle)],
        [0,1,0],
        [math.sin(ry_angle), 0, math.cos(ry_angle)]
    ])

    ## calculate difference in angle between x axis and vector projected onto xy plane

    xy_vector = vector.dot(np.array([
        [1,0,0],
        [0,1,0],
        [0,0,0]
    ]))

    rz_angle = (1 if vector[0] * vector[1] > 0 else -1) * (math.acos(abs(xy_vector[0])/np.linalg.norm(xy_vector)) )
    # print(rz_angle)

    rz = np.array([
        [math.cos(rz_angle), -math.sin(rz_angle),0],
        [math.sin(rz_angle), math.cos(rz_angle), 0],
        [0,0,1]
    ])

    ## combine rotations
    rotation_matrix = rz.dot(ry)
    # print(rotation_matrix.dot(vertices.T).T)

    return rotation_matrix.dot(vertices.T).T

def invert_faces(faces):
    return np.array([tuple(reversed(face)) for face in faces])

def invert_shape_faces(shape):
    return shape[0], invert_faces(shape[1])

def combine_shapes(*shapes):
    if len(shapes) == 0:
        raise ValueError("combine_shapes called with no arguments!")
    if len(shapes) == 1:
        return shapes[0]
    
    shape = (
        np.concatenate((shapes[0][0], shapes[1][0])), # concatenate vertices
        np.concatenate((shapes[0][1], shapes[1][1] + len(shapes[0][0]))) # add length of shape 0 's vertices to all of shape 1 's face points and then concatenate the faces
    )
    return combine_shapes(shape, *shapes[2:])
