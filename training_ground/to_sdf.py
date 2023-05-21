import xmlschema
import os 
from pkg_resources import resource_filename
dir_path = os.path.abspath(resource_filename('training_ground.schemas', 'root.xsd'))
# dir_path = files('training_ground.schema').joinpath('root.xsd')
# dir_path = os.path.dirname(os.path.realpath(__file__)) + '/schemas/root.xsd'

schema = xmlschema.XMLSchema(dir_path)

def to_sdf(obj):
    sdf = schema.encode(obj)
    return sdf

def to_obj(sdf):
    return schema.decode(sdf)

def build_sdf_file(obj, filename):
    xmlschema.XmlDocument(to_sdf(obj), schema).write(filename)