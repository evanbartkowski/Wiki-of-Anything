# user_portal/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.user_portal, name='user_portal'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/', views.view_category_list, name='view_category_list'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('assign-roles/', views.assign_roles, name='assign_roles'),
    path('my-drafts/', views.my_drafts, name='my_drafts'),
    path('media-gallery/', views.media_gallery, name='media_gallery'),
    path('trash/', views.trash, name='trash'),
    path('trash/recover/<int:post_id>/', views.recover_post, name='recover_post'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
