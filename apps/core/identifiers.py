def get_pk(instance_or_id):
    """
    Return primary key integer from either a dict object or integer directly.
    """
    if isinstance(instance_or_id, dict):
        return instance_or_id.get('id')
    return instance_or_id
