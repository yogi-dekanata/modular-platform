def has_role(user, roles):
    """
    Cek apakah user punya salah satu role yang diizinkan.

    :param user: Django user object
    :param roles: list/tuple nama roles yang diizinkan
    :return: True kalau user punya role tersebut, False kalau tidak
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__in=roles).exists()
