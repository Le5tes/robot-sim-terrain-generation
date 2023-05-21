import setuptools

setuptools.setup(
    name='gazebo-training-ground-generator',
    version='0.0.4',
    author='Tim Williamson',
    author_email='timwilliamson1337@gmail.com',
    description='Create terrain for training robots - gazebo',
    packages=['training_ground'],
    include_package_data=True,
    url='git@gitlab.com:ai-masters/final-project/terrain-generation',
    install_requires=['stl', 'xmlschema']
)
