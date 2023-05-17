from to_sdf import build_sdf_file
from terrain_generator import build_terrain

# TODO: pass base path rather than hardcoded to this machine
def build_world(robot):
    sdf_path = '/home/timwilliamson/dev/personal/Online-Msc/dissertation/terrain-generation/world.sdf'

    terrain_path = build_terrain()

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