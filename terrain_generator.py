from to_sdf import to_sdf, to_obj, build_sdf_file
from stl import mesh, Mode
import numpy as np


size = 10

heightmap = np.random.normal(size = (size,size))

plane_vertices = np.array([
    [x,y, heightmap[x,y]]
    for x in range(size)
    for y in range(size)
])

plane_faces = np.array([
    [x, x+1, x+ size] 
    for x in range(size * (size - 1))
    if x % size != size - 1
] + [
    [x+1, x+size, x+ size + 1] 
    for x in range(size * (size - 1))
    if x % size != size - 1
])

plane = mesh.Mesh(np.zeros(plane_faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(plane_faces):
    for j in range(3):
        plane.vectors[i][j] = plane_vertices[f[j],:]

plane.save('plane/plane.stl')

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
                    'pose': '0 0 0 0 0 0',
                    'geometry': {
                        'mesh': {
                            'uri': 'plane.stl',
                            'scale': '1 1 1'
                        }
                    }
                },
                    'collision': {
                    '@name': 'plane_col',
                    'pose': '0 0 0 0 0 0',
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

build_sdf_file(sdf, 'plane/plane.sdf')