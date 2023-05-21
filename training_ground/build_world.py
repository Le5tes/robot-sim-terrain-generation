from training_ground.to_sdf import build_sdf_file
from training_ground.terrain_generator import build_terrain

# TODO: pass base path rather than hardcoded to this machine
def build_world(robot, base_path):
# '/home/timwilliamson/dev/personal/Online-Msc/dissertation/terrain-generation'

    sdf_path = base_path + '/world.sdf'

    terrain_path = build_terrain(base_path)

    sdf = {
        '@version': '1.5',
        'world': {
            '@name': 'rl-world',
            'include': [{
                'uri': terrain_path
            },
            {
                'uri': robot
            }]
        }
    }

    build_sdf_file(sdf, sdf_path)

    return sdf_path

# build_world('/home/timwilliamson/dev/personal/Online-Msc/dissertation/anymal_c_simple_description/urdf/anymal.urdf')