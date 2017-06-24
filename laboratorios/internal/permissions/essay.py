import functools
from . import permission_check


create_essay_check = functools.partial(permission_check, permission='Can add essay')
edit_essay_check = functools.partial(permission_check, permission='Can change essay')
delete_essay_check = functools.partial(permission_check, permission='Can delete essay')