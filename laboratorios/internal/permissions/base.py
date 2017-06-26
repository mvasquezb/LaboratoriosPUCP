import functools


def permission_check(user, permissions):
    if user.is_superuser:
        return True
    if not hasattr(user, 'basicuser'):
        return False
    if not isinstance(permissions, (list, tuple)):
        permissions = [permissions]
    permission_list = user.basicuser.permissions()
    return permission_list.filter(
        codename__in=permissions
    ).exists()


def set_permission_check(permissions):
    return functools.partial(permission_check, permissions=permissions)
