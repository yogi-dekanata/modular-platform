def has_role(user, roles):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__in=roles).exists()
