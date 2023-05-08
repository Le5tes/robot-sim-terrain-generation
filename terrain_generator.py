from to_sdf import to_sdf, to_obj


sdf = {
    '@version': '1.5',
    'model': [
        {'@name': 'bob'}
    ]
}

print(to_sdf(sdf))

# print(to_obj('./testing/test.xml'))