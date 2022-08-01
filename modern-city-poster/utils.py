import hashlib
import base64

def make_hash(o):
    hasher = hashlib.md5()
    hasher.update(repr(make_hashable(o)).encode())
    return hasher.hexdigest()

def make_hashable(o):
    if isinstance(o, (tuple, list)):
        return tuple((make_hashable(e) for e in o))

    if isinstance(o, dict):
        return tuple(sorted((k,make_hashable(v)) for k,v in o.items()))

    if isinstance(o, (set, frozenset)):
        return tuple(sorted(make_hashable(e) for e in o))

    return o