#!/usr/bin/env python3

import os


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laboratorios.settings")
    import django
    django.setup()
    from django.apps import apps
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    from django.db.utils import IntegrityError

    app_label = 'internal'
    Role = apps.get_app_config(app_label).get_model('Role')
    superuser_role = Role.objects.create(
        name='SuperUser'
    )
    superuser_role.permissions.add(*Permission.objects.all())


if __name__ == '__main__':
    main()
