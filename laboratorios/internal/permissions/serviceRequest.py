import functools
from . import permission_check


create_service_request_check = functools.partial(permission_check, permission='Can add service request')
edit_service_request_check = functools.partial(permission_check, permission='Can change service request')
delete_service_request_check = functools.partial(permission_check, permission='Can delete service request')