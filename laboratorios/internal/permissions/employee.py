import functools
from . import permission_check


create_employee_check = functools.partial(permission_check, permission='Can add employee')