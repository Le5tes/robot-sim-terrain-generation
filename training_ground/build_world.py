from training_ground.to_sdf import build_sdf_file
from training_ground.terrain_generator import build_terrain

# TODO: pass base path rather than hardcoded to this machine
def build_world(robot, base_path, t_type = 'jagged', size= 20, intensity = 0.3, robot_contact_base_name = 'anymal::base', rate = 1000, headless = False):
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
            'physics': {
                '@name': '10ms',
                '@type': 'ode',
                'max_step_size': 1.0 / rate,
                'real_time_factor': -1.0 if headless else 1.0
            },
            'plugin': [{
                '@filename': 'libgz-sim7-contact-system',
                '@name': 'gz::sim::systems::Contact'
            },
            {
                '@filename':'libgz-sim7-physics-system',
                '@name':'gz::sim::systems::Physics',
            },
            {
                '@filename':'gz-sim7-scene-broadcaster-system',
                '@name':'gz::sim::systems::SceneBroadcaster'
            }]
        }
    }

    build_sdf_file(sdf, sdf_path)

    return sdf_path

# build_world('/home/timwilliamson/dev/personal/Online-Msc/dissertation/anymal_c_simple_description/urdf/anymal.urdf')