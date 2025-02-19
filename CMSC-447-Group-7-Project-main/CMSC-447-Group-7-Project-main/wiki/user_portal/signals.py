# user_portal/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from user_portal.models import Post, Category
from django.contrib.auth.models import User

@receiver(post_migrate)
def create_roles_and_permissions(sender, **kwargs):
    roles_permissions = {
        'Admin': [
            'add_post', 'change_post', 'delete_post', 'view_post',
            'add_category', 'change_category', 'delete_category', 'view_category',
            'add_user', 'change_user', 'delete_user', 'view_user',
            'add_comment', 'change_comment', 'delete_comment', 'view_comment',
        ],
        'Author': [
            'add_post', 'change_post', 'view_post',
        ],
        'Editor': [
            'change_post', 'view_post', 'add_category', 'change_category',
        ],
        'Moderator': [
            'delete_post', 'delete_comment', 'view_post', 'view_comment',
        ]
    }

    post_content_type = ContentType.objects.get_for_model(Post)
    category_content_type = ContentType.objects.get_for_model(Category)
    user_content_type = ContentType.objects.get_for_model(User)

    for role, permissions in roles_permissions.items():
        group, created = Group.objects.get_or_create(name=role)
        
        for permission in permissions:
            if 'post' in permission:
                content_type = post_content_type
            elif 'category' in permission:
                content_type = category_content_type
            elif 'user' in permission:
                content_type = user_content_type
            else:
                continue
            
            perm, _ = Permission.objects.get_or_create(codename=permission, content_type=content_type)
            group.permissions.add(perm)
