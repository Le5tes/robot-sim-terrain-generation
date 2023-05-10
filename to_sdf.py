import xmlschema

schema = xmlschema.XMLSchema('schemas/root.xsd')

def to_sdf(obj):
    sdf = schema.encode(obj)
    return sdf

def to_obj(sdf):
    return schema.decode(sdf)

def build_sdf_file(obj, filename):
    xmlschema.XmlDocument(to_sdf(obj), schema).write(filename)