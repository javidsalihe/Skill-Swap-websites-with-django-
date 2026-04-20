# skillswap/scripts/init_groups_dynamic.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

def run():
    super_group, _ = Group.objects.get_or_create(name='SuperAdmin')
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    user_group, _ = Group.objects.get_or_create(name='User')

    # get the all model
    all_models = apps.get_models()

    for model in all_models:
        content_type = ContentType.objects.get_for_model(model)
        perms = Permission.objects.filter(content_type=content_type)

        # Admin: just => view + add + change
        for perm in perms:
            if perm.codename in [
                'view_' + model._meta.model_name,
                'add_' + model._meta.model_name,
                'change_' + model._meta.model_name
            ]:
                admin_group.permissions.add(perm)

        # SuperAdmin =>  all permission
        for perm in perms:
            super_group.permissions.add(perm)

        # for perm in perms:
        #     if perm.codename in [
        #
        #     ]
        #     user_group.permissions.add(perm)

    print("Groups and permissions for all models initialized.")
