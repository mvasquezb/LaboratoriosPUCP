import functools
from . import permission_check


create_role_check = functools.partial(permission_check, permission='Can add role')
edit_role_check = functools.partial(permission_check, permission='Can change role')
delete_role_check = functools.partial(permission_check, permission='Can delete role')