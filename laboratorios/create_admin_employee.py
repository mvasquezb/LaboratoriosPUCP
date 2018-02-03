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
    from django.contrib.auth.models import User

    app_label = 'internal'
    app_config = apps.get_app_config(app_label)
    Employee = app_config.get_model('Employee')
    Role = app_config.get_model('Role')

    superuser = User.objects.get(username='admin')
    admin_role = Role.objects.get(name='SuperUser')
    admin = Employee.objects.create(
        user=superuser
    )
    admin.roles.add(admin_role)


if __name__ == '__main__':
    main()
