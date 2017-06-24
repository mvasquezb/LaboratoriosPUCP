import functools
from . import permission_check


edit_service_contract_check = functools.partial(permission_check, permission='Can change service contract')
delete_service_contract_check = functools.partial(permission_check, permission='Can delete service contract')