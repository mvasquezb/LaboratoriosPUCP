import functools
from . import permission_check


create_sample_type_check = functools.partial(permission_check, permission='Can add sample type')
edit_sample_type_check = functools.partial(permission_check, permission='Can change sample type')
delete_sample_type_check = functools.partial(permission_check, permission='Can delete sample type')