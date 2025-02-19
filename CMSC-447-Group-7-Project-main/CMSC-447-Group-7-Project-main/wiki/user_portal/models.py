# models.py (user_portal)
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)  # or ForeignKey to the User model if author is linked to users
    tags = models.CharField(max_length=255, blank=True, null=True)  # Use ManyToManyField if you need multiple tags
    body = RichTextField()
    meta_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)  # New status field for Draft/Published
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class MediaFile(models.Model):
    file = models.ImageField(upload_to='media/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_profile_pic.png', blank=True)



    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()