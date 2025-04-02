from django.urls import path
from users.views import new_post_view, home_page, index_page, login_page, logout_page, signup_view, posts_page
from . import views

urlpatterns = [
    
    path('', index_page, name="index"),
    path('login/', login_page, name="login"),
    path('logout/', logout_page, name="logout"),
    path('signup/', signup_view, name="signup"),
    path('posts/', posts_page, name="posts"),
    path('chatter/', home_page, name="home"),  # ✅ Updated this line
    path('posts/new/', new_post_view, name='new_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
        path('elyse/', views.go_to_chat_with_user5, name='go-to-user5-chat'),
        # Add these to your urlpatterns
path('souls/', views.souls_tunnel, name='souls-tunnel'),
path('tunnel/', views.go_to_souls, name='go-to-souls'),
path('souls/', views.souls_tunnel, name='souls-tunnel'),
path('add-memory/', views.add_memory, name='add-memory'),
path('tunnel/', views.go_to_souls, name='go-to-souls'),

]
