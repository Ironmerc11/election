def parse(string):
    d = {'True': True, 'False': False}
    return d.get(string, string)