# admin.py
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from user_portal.models import Post, Category

# Extend User model to assign roles via Groups
class UserAdminWithGroups(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['groups'].help_text = "Assign user roles (e.g. Admin, Author, Moderator, Editor)"
        return form

admin.site.unregister(User)
admin.site.register(User, UserAdminWithGroups)

def create_roles_and_assign_permissions():
    # Define the roles and associated permissions
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

    # Get the content types for Post, Category, and User models
    post_content_type = ContentType.objects.get_for_model(Post)
    category_content_type = ContentType.objects.get_for_model(Category)
    user_content_type = ContentType.objects.get_for_model(User)

    # Create groups if they don't exist and assign permissions
    for role, permissions in roles_permissions.items():
        group, created = Group.objects.get_or_create(name=role)
        
        for permission in permissions:
            # Get or create permission based on the content type and codename
            if permission.startswith('add_') or permission.startswith('change_') or permission.startswith('delete_') or permission.startswith('view_'):
                # Determine which content type this permission is for
                if 'post' in permission:
                    content_type = post_content_type
                elif 'category' in permission:
                    content_type = category_content_type
                elif 'user' in permission:
                    content_type = user_content_type
                else:
                    continue  # Skip if no matching content type
                
                perm, _ = Permission.objects.get_or_create(codename=permission, content_type=content_type)
                group.permissions.add(perm)

# Call the function to create roles and assign permissions
create_roles_and_assign_permissions()
