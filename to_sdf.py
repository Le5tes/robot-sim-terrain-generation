import xmlschema

schema = xmlschema.XMLSchema('schemas/root.xsd')

def to_sdf(object):
    sdf = schema.encode(object)
    return sdf

def to_obj(sdf):
    return schema.decode(sdf)