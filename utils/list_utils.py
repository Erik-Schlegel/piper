
def merge_named_lists(list_a, list_b):
    """
    Merges two lists of dictionaries, keeping items from list_a when 'name' conflicts exist.

    Args:
        list_a: Primary list of dicts with 'name' field
        list_b: Secondary list of dicts with 'name' field

    Returns:
        List of merged dictionaries with no duplicate names
    """
    name_map = {item['name']: item for item in list_a}

    # Only add items from list_b if their name isn't already present
    for item in list_b:
        if item['name'] not in name_map:
            name_map[item['name']] = item

    return list(name_map.values())