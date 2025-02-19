# user_portal/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from .forms import PostForm, CategoryForm, ProfileForm
from .models import Profile, Post, Category, MediaFile 
from django.db.models import ProtectedError
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator

@login_required
def user_portal(request):
    posts = Post.objects.all()  # Adjust the filter condition as needed
    return render(request, 'user_portal/user_portal.html', {'posts': posts})  

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.status = request.POST.get('status', 'DRAFT')  # Save as draft or publish based on the button clicked
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'user_portal/create_post.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()  # You may add filtering or pagination as needed
    return render(request, 'user_portal/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    tags = [tag.strip() for tag in post.tags.split(',')]
    
    # Find related posts based on category or tags (excluding the current post)
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:3]
    
    return render(request, 'user_portal/post_detail.html', {
        'post': post,
        'tags': tags,
        'related_posts': related_posts
    })

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
        
    else:
        form = PostForm(instance=post)
    
    return render(request, 'user_portal/edit_post.html', {'form': form, 'post': post})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')  # Redirect to the post list after deletion
    
    # Render the delete confirmation template for GET requests
    return render(request, 'user_portal/delete_post.html', {'post': post})


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'user_portal/create_category.html', {'form': form})

def view_category_list(request):
    categories = Category.objects.all()
    return render(request, 'user_portal/view_category_list.html', {'categories': categories})

def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('view_category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'user_portal/edit_category.html', {'form': form, 'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    try:
        category.delete()
    except ProtectedError:
        # Handle case where category is linked to posts
        # we set post categories to None
        Post.objects.filter(category=category).update(category=None)
    
    return redirect('view_category_list')

@login_required
@user_passes_test(lambda u: u.is_superuser)  # Only allow Admin to access this view
def assign_roles(request):
    users = User.objects.all()
    groups = Group.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_name = request.POST.get('group')

        user = User.objects.get(id=user_id)
        group = Group.objects.get(name=group_name)

        # Remove user from all groups and add to selected group
        user.groups.clear()
        user.groups.add(group)

        return redirect('assign_roles')

    return render(request, 'user_portal/assign_roles.html', {
        'users': users,
        'groups': groups,
    })

def my_drafts(request):
    # Get all drafts by the current user
    drafts = Post.objects.filter(status='DRAFT', author=request.user.username)
    return render(request, 'user_portal/my_drafts.html', {'drafts': drafts})


def media_gallery(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'uploaded_at')  # Default sorting by upload date
    media_files = MediaFile.objects.all()

    # Filter by search query
    if query:
        media_files = media_files.filter(name__icontains=query)

    # Sorting
    media_files = media_files.order_by(sort_by)

    # Pagination
    paginator = Paginator(media_files, 12)  # Show 12 media files per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_portal/media_gallery.html', {
        'media_files': page_obj,
        'query': query,
        'sort_by': sort_by
    })

# View deleted posts in Trash
def trash(request):
    deleted_posts = Post.objects.filter(deleted=True)
    return render(request, 'user_portal/trash.html', {'deleted_posts': deleted_posts})

# Recover post
def recover_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.deleted:
        post.deleted = False
        post.save()
    return redirect('trash')

# To recover a group of posts
def batch_recover(request):
    if request.method == 'POST':
        post_ids = request.POST.getlist('post_ids')  # Get selected post IDs
        if post_ids:
            posts = Post.objects.filter(id__in=post_ids, is_deleted=True)  # Only recover deleted posts
            posts.update(is_deleted=False)  # Mark as not deleted
    return redirect('trash')  # Redirect to trash page

@login_required
def profile_view(request):
    profile = request.user.profile  # Access the profile of the logged-in user
    return render(request, 'user_portal/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user_portal/edit_profile.html', {'form': form})
