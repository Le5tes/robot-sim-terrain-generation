from training_ground.to_sdf import build_sdf_file
from stl import mesh, Mode
import os
import numpy as np

terrain_fns = {
    'jagged': jagged_terrain,
    'boxes': boxes_terrain
}


def build_terrain(base_path, t_type, size, intensity):
    path = base_path + '/plane'


    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    stl_path = path + '/plane.stl'
    sdf_path = path + '/plane.sdf'

    plane_vertices, plane_faces = terrain_fns[t_type](size, intensity)

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

    with open(path + '/model.config', 'w') as f:
        f.write('''
<?xml version="1.0"?>

<model>
  <name>Generated Training Ground</name>
  <version>1.0</version>
  <sdf version="1.5">plane.sdf</sdf>

  <author>
    <name>Tim Williamson</name>
    <email>tw964@bath.ac.uk</email>
  </author>

  <description>
	A procedurally generated terrain
  </description>
</model>
        ''')

    build_sdf_file(sdf, sdf_path)

    return sdf_path

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

