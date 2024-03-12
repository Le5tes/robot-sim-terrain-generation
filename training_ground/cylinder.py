import numpy as np
import math

from training_ground.shape_utils import rotate_to_follow_vector

## Generates vertices for a cylinder oriented in the z axis
# Number of points returned = (resolution + 1) * 2 
def create_vertical_cylinder_vertices(radius, length, resolution):
    origin = np.array([0,0,0])
    first_point = np.array([radius,0,0])
    lower_circle = []
    lower_circle.append(origin)
    for i in range(resolution):
        angle = i * 2 * math.pi / resolution
        rotation = np.array([
            [math.cos(angle), -math.sin(angle),0],
            [math.sin(angle), math.cos(angle), 0],
            [0,0,1]
        ])
        lower_circle.append(rotation.dot(first_point.T))
    lower_circle = np.array(lower_circle)
    upper_circle = lower_circle + np.array([0,0,length])
    return np.concatenate((lower_circle, upper_circle))

def generate_cylinder_bottom_faces(resolution):
    faces = []
    for i in range(resolution - 1):
        faces.append([0,i+2, i+1])
    faces.append([0,1, resolution])
    return np.array(faces)

def generate_cylinder_top_faces(resolution):
    faces = []
    for i in range(resolution - 1):
        faces.append([0,i+1, i+2])
    faces.append([0, resolution, 1])
    return np.array(faces) + resolution + 1

def generate_cylinder_side_faces(resolution):
    faces = []
    for i in range(resolution - 1):
        faces.append([i + 1, i + 2, i + 2 + resolution])
        faces.append([i + 2, i + 3 + resolution, i + 2 + resolution])
    faces.append([resolution, 1, resolution * 2 + 1])
    faces.append([1, resolution + 2, resolution * 2 + 1])
    return np.array(faces)


def generate_cylinder_faces(resolution):
    return np.concatenate((
        generate_cylinder_bottom_faces(resolution),
        generate_cylinder_side_faces(resolution),
        generate_cylinder_top_faces(resolution)
    ))


def create_cylinder(radius, start, end, resolution):
    vector = end-start
    length = np.linalg.norm(vector)

    vertical_cylinder = create_vertical_cylinder_vertices(radius, length, resolution)
    rotated_cylinder = rotate_to_follow_vector(vector, vertical_cylinder)
    final_cylinder_vertices = rotated_cylinder + start

    faces = generate_cylinder_faces(resolution)

    pole_start = final_cylinder_vertices[0]
    pole_end = final_cylinder_vertices[resolution + 1]
    print(pole_start, pole_end, np.linalg.norm(pole_end-pole_start))
    print()
    return final_cylinder_vertices, faces
