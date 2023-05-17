from to_sdf import build_sdf_file
from stl import mesh, Mode
import numpy as np


def build_terrain():

    stl_path = '/home/timwilliamson/dev/personal/Online-Msc/dissertation/terrain-generation/plane/plane.stl'
    sdf_path = '/home/timwilliamson/dev/personal/Online-Msc/dissertation/terrain-generation/plane/plane.sdf'

    size = 20
    jaggedness = 0.3

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

    plane = mesh.Mesh(np.zeros(plane_faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(plane_faces):
        for j in range(3):
            plane.vectors[i][j] = plane_vertices[f[j],:]

    plane.save(stl_path)

    sdf = {
        '@version': '1.5',
        'model': [
            {
                '@name': 'plane', 
                'static': True,
                'link': {
                    '@name':'plane_link',
                    'visual': {
                        '@name': 'plane_visual',
                        'pose': '-10 -10 -1 0 0 0',
                        'geometry': {
                            'mesh': {
                                'uri': 'plane.stl',
                                'scale': '1 1 1'
                            }
                        }
                    },
                        'collision': {
                        '@name': 'plane_col',
                        'pose': '-10 -10 -1 0 0 0',
                        'geometry': {
                            'mesh': {
                                'uri': 'plane.stl',
                                'scale': '1 1 1'
                            }
                        }
                    }
                }
            }
        ]
    }

    build_sdf_file(sdf, sdf_path)

    return sdf_path