from training_ground.to_sdf import build_sdf_file
from training_ground.terrain_generators import jagged_terrain, boxes_terrain
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
