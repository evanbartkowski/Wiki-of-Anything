# templatetags/custom_filters.py
from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    # Check if the field is a BoundField (widget) and has `as_widget` method
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css})
    # Otherwise, just return the field as it is
    return field

@register.filter
def show_sidebar(url_name):
    # Define the list of URL names where you want to show the sidebar
    sidebar_urls = [
        'user_portal', 'create_post', 'post_list', 'post_detail', 'edit_post',
        'delete_post', 'create_category', 'view_category_list', 'edit_category',
        'delete_category', 'assign_roles', 'my_drafts', 'media_gallery', 
        'trash', 'profile', 'edit_profile'
    ]
    return url_name in sidebar_urls
