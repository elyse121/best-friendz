from django.contrib import admin
from .models import Message, GroupChat  # Import GroupChat model

admin.site.register(Message)
admin.site.register(GroupChat)  # Register GroupChat model
