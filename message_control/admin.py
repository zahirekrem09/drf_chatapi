from django.contrib import admin

from .models import Message, MessageAttachment

admin.site.register((Message, MessageAttachment))
