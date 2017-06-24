import functools
from . import permission_check


create_inventory_order_check = functools.partial(permission_check, permission='Can add inventory order')
edit_inventory_order_check = functools.partial(permission_check, permission='Can change inventory order')
delete_inventory_order_check = functools.partial(permission_check, permission='Can delete inventory order')