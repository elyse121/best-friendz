from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Post, Like, Comment, UserProfile, Memory

# --- CHAT REDIRECT ---
@login_required
def go_to_chat_with_user5(request):
    user5 = get_object_or_404(User, id=5)
    return redirect('chat', room_name=user5.username)

@login_required
def redirect_to_user5_chat(request):
    user = get_object_or_404(User, id=5)
    return redirect('chat', room_name=user.username)

# --- POST LIKES ---
@require_POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_obj, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    like_count = post.likes.count()
    return JsonResponse({'liked': liked, 'like_count': like_count})

# --- COMMENTS ---
@login_required
def comment_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        comment_content = request.POST.get('comment')
        if comment_content:
            Comment.objects.create(post=post, content=comment_content, user=request.user)
        return redirect('posts')

# --- CREATE POST ---
@login_required
def new_post_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        photo = request.FILES.get('photo')

        if photo:
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            Post.objects.create(author=request.user, title=title, content=content, photo=filename)
        else:
            Post.objects.create(author=request.user, title=title, content=content)

        return redirect('posts')

    return render(request, 'new_post.html')

# --- DISPLAY POSTS ---
@login_required
def posts_page(request):
    posts = Post.objects.all().order_by('-created_at')
    user_liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'posts.html', {
        'posts': posts,
        'user_liked_post_ids': user_liked_post_ids,
    })

# --- HOMEPAGE ---
@login_required
def home_page(request):
    return render(request, 'chat.html')

# --- INDEX PAGE ---
def index_page(request):
    return render(request, 'index.html')

# --- LOGIN ---
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('posts')
        else:
            messages.error(request, 'Invalid email or password.')
    if request.user.is_authenticated:
        return redirect('posts')
    return render(request, 'login.html')

# --- LOGOUT ---
@login_required
def logout_page(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')

# --- SIGNUP ---
def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')

        if password1 != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user_profile = UserProfile.objects.get(user=user)
        if profile_picture:
            user_profile.profile_picture = profile_picture
            user_profile.save()

        messages.success(request, 'Signup successful! You can now log in.')
        return redirect('login')

    if request.user.is_authenticated:
        return redirect('posts')
    return render(request, 'signup.html')

# --- SOULS (MEMORY WALL) ---

@login_required
def souls_tunnel(request):
    # ✅ UPDATED: fetch all memories from all users, not just the current user
    memories = Memory.objects.all().order_by('-created_at')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        memories_data = [{
            'id': memory.id,
            'name': memory.name,
            'image_url': memory.image.url,
            'caption': memory.caption,
            'created_at': memory.created_at.strftime("%b %d, %Y %I:%M %p")
        } for memory in memories]
        return JsonResponse({'memories': memories_data})

    return render(request, 'souls.html', {'memories': memories})

@login_required
@require_POST
def add_memory(request):
    name = request.POST.get('name')
    caption = request.POST.get('caption')
    image = request.FILES.get('image')

    if not all([name, caption, image]):
        return JsonResponse({'status': 'error', 'message': 'All fields are required'})

    memory = Memory.objects.create(
        user=request.user,
        name=name,
        caption=caption,
        image=image
    )

    return JsonResponse({
        'status': 'success',
        'memory': {
            'id': memory.id,
            'name': memory.name,
            'image_url': memory.image.url,
            'caption': memory.caption,
            'created_at': memory.created_at.strftime("%b %d, %Y %I:%M %p")
        }
    })

@login_required
def go_to_souls(request):
    return redirect('souls-tunnel')
