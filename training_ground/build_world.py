from training_ground.to_sdf import build_sdf_file
from training_ground.terrain_generator import build_terrain

# TODO: pass base path rather than hardcoded to this machine
def build_world(robot, base_path, t_type = 'jagged', size= 20, intensity = 0.3, robot_contact_base_name = 'anymal::base'):
# '/home/timwilliamson/dev/personal/Online-Msc/dissertation/terrain-generation'

    sdf_path = base_path + '/world.sdf'

    terrain_path = build_terrain(base_path, t_type, size, intensity, robot_contact_base_name)

    sdf = {
        '@version': '1.5',
        'world': {
            '@name': 'rl_world',
            'include': [ 
                {'uri': terrain_path},
                {'uri': robot}
            ],
            'plugin': {
                '@filename': 'libignition-gazebo6-contact-system',
                '@name': 'ignition::gazebo::systems::Contact'
            },
            'plugin': {
                '@filename':'libignition-gazebo6-physics-system',
                '@name':'ignition::gazebo::systems::Physics'
            },
            'plugin': {
                '@filename':'libignition-gazebo6-scene-broadcaster-system',
                '@name':'ignition::gazebo::systems::SceneBroadcaster'
            }
        }
    }

    build_sdf_file(sdf, sdf_path)

    return sdf_path

# build_world('/home/timwilliamson/dev/personal/Online-Msc/dissertation/anymal_c_simple_description/urdf/anymal.urdf')