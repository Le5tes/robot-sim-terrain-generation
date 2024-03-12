from training_ground.to_sdf import build_sdf_file
from training_ground.terrain_generator import build_terrain, Point


def build_world(robot, base_path, t_type = 'jagged', size= 20, intensity = 0.3, start = Point(10,3), goal = Point(10,17), robot_contact_base_name = 'anymal::base', rate = 1000, headless = False, bound = False):
    sdf_path = base_path + '/world.sdf'

    terrain_path, voxels = build_terrain(base_path, t_type, size, intensity, robot_contact_base_name, start, goal, bound)

    sdf = {
        '@version': '1.5',
        'world': {
            '@name': 'rl_world',
            'include': [ 
                {'uri': terrain_path},
                {
                    'uri': robot,
                    'pose': f"{start.x - size/2} {start.y - size/2} 0 0 0 0"
                }
            ],
            'physics': {
                '@name': '10ms',
                '@type': 'ode',
                'max_step_size': 1.0 / rate,
                'real_time_factor': -1.0 if headless else 1.0
            },
            'plugin': [{
                '@filename': 'libignition-gazebo6-contact-system',
                '@name': 'ignition::gazebo::systems::Contact'
            },
            {
                '@filename':'libignition-gazebo6-physics-system',
                '@name':'ignition::gazebo::systems::Physics',
            },
            {
                '@filename':'libignition-gazebo6-scene-broadcaster-system',
                '@name':'ignition::gazebo::systems::SceneBroadcaster'
            }]
        }
    }

    build_sdf_file(sdf, sdf_path)

    return sdf_path, voxels
