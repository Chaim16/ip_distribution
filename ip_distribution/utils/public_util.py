import hashlib


def hash_encryption(s, salt="ip_distribution"):
    h = hashlib.sha3_256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
