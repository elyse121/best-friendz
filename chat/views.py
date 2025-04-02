from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import GroupChat

@login_required
def group_chat_view(request):
    search_query = request.GET.get("search", "")

    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            GroupChat.objects.create(sender=request.user, message=message)

    # Fetch all group messages
    messages = GroupChat.objects.all().order_by("timestamp")

    if search_query:
        messages = messages.filter(Q(message__icontains=search_query))

    return render(request, "group_chat.html", {"messages": messages, "search_query": search_query})



@login_required
def redirect_to_user5_chat(request):
    user5 = get_object_or_404(User, id=5)
    return redirect('chat', room_name=user5.username)

def user_profile_view(request, username):
    user = User.objects.get(username=username)
    return render(request, 'user_profile.html', {'profile_user': user})

@login_required
def chat_room(request, room_name):
    search_query = request.GET.get('search', '') 
    users = User.objects.exclude(id=request.user.id)  # Get all users except current

    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    chats = chats.order_by('timestamp') 

    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message  # can be None
        })

    # Sort: Users with messages first (by latest timestamp), then users with no messages
    # Sort: Users with messages first (by latest timestamp), then users with no messages
    user_last_messages.sort(
    key=lambda x: x['last_message'].timestamp.timestamp() if x['last_message'] else 0,
    reverse=True
)



    # ✅ Special Chatter room logic
    context = {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query
    }

    if room_name == 'chatter':
        context['special_message'] = 'Welcome to the Chatter Room!'  # Optional message

    return render(request, 'chat.html', context)
