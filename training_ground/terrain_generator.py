from training_ground.to_sdf import build_sdf_file
from training_ground.terrain_generators import jagged_terrain, boxes_terrain, path_terrain, pillars_terrain, potholes_terrain, stairs_terrain
from stl import mesh, Mode
from madcad.mesh import Mesh, numpy_to_typedlist
from madcad.mathutils import typedlist, vec3, uvec3
from madcad.hashing import PositionMap
from collections import namedtuple
import os
import numpy as np

terrain_fns = {
    'jagged': jagged_terrain,
    'boxes': boxes_terrain,
    'stairs': stairs_terrain,
    'holes': potholes_terrain,
    'pillars': pillars_terrain,
    'path': path_terrain
}

Point = namedtuple('Point', ['x','y'])

def create_voxels(stlmesh):
    trinum = stlmesh.points.shape[0]
    mesh = Mesh(
			numpy_to_typedlist(stlmesh.points.reshape(trinum*3, 3), vec3), 
			typedlist(uvec3(i, i+1, i+2)  for i in range(0, 3*trinum, 3)),
		)

    size = 0.1
    voxels = set()
    hasher = PositionMap(size)   # ugly object creation, just to use one of its methods
    for face in mesh.faces:
        voxels.update(hasher.keysfor(mesh.facepoints(face)))
    return {(voxel[0], voxel[1],voxel[2] + 100) for voxel in voxels if voxel[2] >= -100 and voxel[2] < 100}

def plane_and_voxels(t_type, size, intensity, start, goal):
    if not t_type in terrain_fns:
        raise ValueError("Terrain type argument (t_type) not recognised. Options are:" + str(list(terrain_fns)))
    
    plane_vertices, plane_faces = terrain_fns[t_type](size, intensity, start, goal)

    plane = mesh.Mesh(np.zeros(plane_faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(plane_faces):
        for j in range(3):
            plane.vectors[i][j] = plane_vertices[f[j],:]

    voxels = create_voxels(plane)

    return plane, voxels

def build_terrain(base_path, t_type, size, intensity, robot_contact_base_name, start, goal):
    path = base_path + '/plane'

    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    stl_path = path + '/plane.stl'
    sdf_path = path + '/plane.sdf'

    plane, voxels = plane_and_voxels(t_type, size, intensity, start, goal)

    plane.save(stl_path)

    sdf = {
        '@version': '1.5',
        'model': [
            {
                '@name': 'plane', 
                'static': True,
                'link': [{
                    '@name':'plane_link',
                    'visual': {
                        '@name': 'plane_visual',
                        'pose': f"{-size/2} {-size/2} -1 0 0 0",
                        'geometry': {
                            'mesh': {
                                'uri': 'plane.stl',
                                'scale': '1 1 1'
                            }
                        },
                        'material': {
                            'ambient': '0.8 0.8 0.8 1',
                            'diffuse': '0.8 0.8 0.8 1',
                            'specular': '0.8 0.8 0.8 1'
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
                    },
                    'sensor': {
                        '@name': 'touch_sensor',
                        '@type': 'contact',
                        'contact': {
                            'collision': 'plane_col'
                        }
                    }
                },
                {
                    '@name':'start',
                    'visual': {
                        '@name': 'start_visual',
                        'pose': f"{start.x - size/2} {start.y - size/2} -3 0 0 0",
                        'geometry': {
                            'cylinder': {
                                'radius': 0.5,
                                'length': 10.0
                            }
                        },
                        'cast_shadows':False,
                        'material': {
                            'ambient': '1 0 0 0.5',
                            'diffuse': '1 0 0 0.5',
                            'specular': '1 0 0 0'
                        }
                    },
                },
                {
                    '@name':'goal',
                    'visual': {
                        '@name': 'goal_visual',
                        'pose': f"{goal.x - 10} {goal.y - 10} -3 0 0 0",
                        'geometry': {
                            'cylinder': {
                                'radius': 0.5,
                                'length': 10.0
                            }
                        },
                        'cast_shadows':False,
                        'material': {
                            'ambient': '0 0 1 0.5',
                            'diffuse': '0 0 1 0.5',
                            'specular': '1 0 0 0'
                        }
                    },
                }],
                'plugin': {
                    '@filename': 'ignition-gazebo-touchplugin-system',
                    '@name': 'ignition::gazebo::systems::TouchPlugin',
                    'target': robot_contact_base_name,
                    'namespace': 'floor',
                    'time': 0.001,
                    'enabled': 'true'
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

    return sdf_path, voxels
