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
    app_models = apps.get_app_config(app_label).get_models()
    ctype_list = ContentType.objects.filter(app_label=app_label)
    for model in app_models:
        model_name = model._meta.label[len(app_label) + 1:]
        model_lower = model_name.lower()
        verbose_name = model._meta.verbose_name
        ctype = ctype_list.get(app_label=app_label, model=model_lower)
        # perm_list = Permission.objects.filter(content_type=ctype)
        index_perm_name = 'Can show {} index'.format(verbose_name)
        index_perm_codename = 'index_{}'.format(model_lower)
        show_perm_name = 'Can show {} detail'.format(verbose_name)
        show_perm_codename = 'show_{}'.format(model_lower)
        try:
            Permission.objects.create(
                content_type=ctype,
                codename=index_perm_codename,
                name=index_perm_name
            )
        except IntegrityError:
            pass
        try:
            Permission.objects.create(
                content_type=ctype,
                codename=show_perm_codename,
                name=show_perm_name
            )
        except IntegrityError:
            pass
        if model_name == 'ServiceContract':
            try:
                Permission.objects.create(
                    content_type=ctype,
                    codename='approve_servicecontract',
                    name='Can approve servicecontract'
                )
            except IntegrityError:
                pass
            try:
                Permission.objects.create(
                    content_type=ctype,
                    codename='refuse_servicecontract',
                    name='Can refuse servicecontract'
                )
            except IntegrityError:
                pass


if __name__ == '__main__':
    main()
