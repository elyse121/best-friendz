from django.urls import path
from . import views  # Import views correctly

urlpatterns = [
    path('<str:room_name>/', views.chat_room, name='chat'),
    path('elyse/', views.redirect_to_user5_chat, name='go-to-user5-chat'),
    path('group/chat/', views.group_chat_view, name='group_chat'),  # Updated path
    
]
