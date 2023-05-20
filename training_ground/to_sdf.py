import xmlschema
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

schema = xmlschema.XMLSchema(dir_path + '/schemas/root.xsd')

def to_sdf(obj):
    sdf = schema.encode(obj)
    return sdf

def to_obj(sdf):
    return schema.decode(sdf)

def build_sdf_file(obj, filename):
    xmlschema.XmlDocument(to_sdf(obj), schema).write(filename)