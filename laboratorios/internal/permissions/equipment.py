import functools
from . import permission_check


create_equipment_check = functools.partial(permission_check, permission='Can add equipment')
edit_equipment_check = functools.partial(permission_check, permission='Can change equipment')
delete_equipment_check = functools.partial(permission_check, permission='Can delete equipment')