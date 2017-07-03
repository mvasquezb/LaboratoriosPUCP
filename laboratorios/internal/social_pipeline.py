from django.contrib.auth.models import User


def test_basicuser(*args, **kwargs):
    backend = kwargs.get('backend')
    request_data = backend.strategy.request_data()
    print(request_data)
    details = kwargs.get('details')
    print(details)
    if details.get('email'):
        try:
            user = User.objects.get(email=details.get('email'))
        except User.DoesNotExist:
            msg = ('No existe un usuario registrado con ese correo.' +
                   ' Por favor intente con un correo diferente')
            backend.strategy.session_set('auth_message', msg)
            user = None
            return {'user': user}
        except User.MultipleObjectsReturned:
            msg = ('Existe más de un usuario registrado con ese correo.' +
                   ' Por favor intente con otro correo')
            user = None
            return {'user': user}

    if user is None:
        user = kwargs.get('user')
    if user is None:
        return {'user': user}

    if not user.is_active or (hasattr(user, 'basicuser') and
                              user.basicuser.deleted):
        msg = ('Este usuario está deshabilitado.' +
               ' Por favor intente con un usuario diferente')
        backend.strategy.session_set('auth_message', msg)
        user = None
    elif hasattr(user, 'basicuser') and hasattr(user.basicuser, 'client'):
        msg = ('El módulo del cliente está en construcción.' +
               ' Por favor intente con un usuario diferente')
        backend.strategy.session_set('auth_message', msg)
        user = None
    return {
        'user': user,
    }
