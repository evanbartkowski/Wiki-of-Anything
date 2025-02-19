# forms.py (user_portal)
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post, Category, Profile 

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(config_name='default'))
    class Meta:
        model = Post
        fields = ['title', 'meta_title', 'author', 'tags', 'body', 'meta_description', 'image', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400'}),
            'meta_title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400'}),
            'author': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400'}),
            'tags': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400'}),
            'meta_description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full px-3 py-2 text-gray-600 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-400',
                'placeholder': 'Enter category name'
            })
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'w-full px-3 py-2 text-gray-600 border border-gray-300 rounded-md'}),
        }


