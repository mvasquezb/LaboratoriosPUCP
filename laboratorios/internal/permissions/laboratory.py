import functools
from . import permission_check


create_laboratory_check = functools.partial(permission_check, permission='Can add laboratory')
edit_laboratory_check = functools.partial(permission_check, permission='Can change laboratory')
delete_laboratory_check = functools.partial(permission_check, permission='Can delete laboratory')