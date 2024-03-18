import numpy as np

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