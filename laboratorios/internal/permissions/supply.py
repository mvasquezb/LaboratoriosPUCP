import functools
from . import permission_check


create_supply_check = functools.partial(permission_check, permission='Can add supply')
edit_supply_check = functools.partial(permission_check, permission='Can change supply')
delete_supply_check = functools.partial(permission_check, permission='Can delete supply')