from django.contrib import admin
from .models import CustomUser, Jwt, Favorite, UserProfile

admin.site.register((CustomUser, UserProfile, Favorite, Jwt))
