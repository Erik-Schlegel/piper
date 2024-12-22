
def deep_merge(dict1, dict2):
    """
    Recursively merges two dictionaries, keeping values from dict2 when conflicts exist.
    """
    for key in dict2:
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            deep_merge(dict1[key], dict2[key])
        else:
            dict1[key] = dict2[key]
    return dict1