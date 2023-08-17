import setuptools

setuptools.setup(
    name='gazebo-training-ground-generator',
    version='0.0.19',
    author='Tim Williamson',
    author_email='timwilliamson1337@gmail.com',
    description='Create terrain for training robots - gazebo',
    packages=['training_ground', 'training_ground.schemas'],
    package_data={
        "training_ground.schemas": ["*.xsd"],
    },
    url='git@gitlab.com:ai-masters/final-project/terrain-generation',
    install_requires=['numpy-stl', 'xmlschema']
)
