import functools


def permission_check(user, permission):
    if not hasattr(user, 'basicuser'):
        return False
    return permission in user.basicuser.permissions()


def set_permission_check(permission):
    return functools.partial(permission_check, permission=permission)
