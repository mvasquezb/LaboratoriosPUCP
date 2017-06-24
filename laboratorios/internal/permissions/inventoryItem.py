import functools
from . import permission_check


delete_inventory_item_check = functools.partial(permission_check, permission='Can delete inventory item')
edit_inventory_item_check = functools.partial(permission_check, permission='Can change inventory item')