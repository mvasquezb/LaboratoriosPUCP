from social_core.exceptions import AuthException


def test_basicuser(*args, **kwargs):
    user = kwargs.get('user')
    if user:
        raise AuthException('El usuario no existe')
    if not hasattr(user, 'basicuser'):
        raise AuthException('Este usuario no es válido')

