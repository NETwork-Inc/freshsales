from os import path
import json

def clean(d):
    if isinstance(d, dict):
        d1 = {}
        for k in d.keys():
            v = d[k]
            if isinstance(v, dict):
                v = clean(v)
            elif isinstance(v, int):
                v = 0
            elif isinstance(v, float):
                v = 0.0
            elif isinstance(v, list):
                v = clean(v)
            else:
                v = 'xxx'
            d1[k] = v
        return d1
    elif isinstance(d, list):
        d1 = []
        for v in d:
            d1.append(clean(v))
        return d1
    return d

def dict_read(filename):
    basepath = path.dirname(__file__)
    filepath = path.join(basepath, filename)
    json_str = open(filepath, 'r').read()
    return json.loads(json_str)

def dict_compare_keys(d1, d2, key_path=''):
    ''' Compare two dicts recursively and see if dict1 has any keys that dict2 does not
    Returns: list of key paths
    '''
    res = []
    if not d1:
        return res
    if not isinstance(d1, dict):
        return res
    for k in d1:
        if k not in d2:
            missing_key_path = f'{key_path}->{k}'
            res.append(missing_key_path)
        else:
            if isinstance(d1[k], dict):
                key_path1 = f'{key_path}->{k}'
                res1 = dict_compare_keys(d1[k], d2[k], key_path1)
                res = res + res1
            elif isinstance(d1[k], list):
                key_path1 = f'{key_path}->{k}[0]'
                dv1 = d1[k][0] if len(d1[k]) > 0 else None
                dv2 = d2[k][0] if len(d2[k]) > 0 else None
                res1 = dict_compare_keys(dv1, dv2, key_path1)
                res = res + res1
    return res