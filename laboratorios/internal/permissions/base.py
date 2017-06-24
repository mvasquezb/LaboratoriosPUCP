def permission_check(user, permission):
    if not hasattr(user, 'basicuser'):
        return False
    return permission in user.basicuser.permissions()