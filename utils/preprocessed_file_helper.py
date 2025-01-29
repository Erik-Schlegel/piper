import os
import json
import hashlib


_PREPROCESSED_FOLDER = 'resources/preprocessed'


def _get_hash(obj):
    obj_str = json.dumps(obj, sort_keys=True)
    hash_obj = hashlib.sha256(obj_str.encode('utf-8'))
    return hash_obj.hexdigest()


def get_hashed_path(obj):
    return f"{_PREPROCESSED_FOLDER}/{_get_hash(obj)}"


def is_hashed_path_existing(obj):
    return os.path.exists(get_hashed_path(obj))
