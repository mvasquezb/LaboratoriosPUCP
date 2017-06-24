import functools
from . import permission_check


create_essay_method_check = functools.partial(permission_check, permission='Can add essay method')
edit_essay_method_check = functools.partial(permission_check, permission='Can change essay method')
delete_essay_method_check = functools.partial(permission_check, permission='Can delete essay method')