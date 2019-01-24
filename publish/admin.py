from django.contrib import admin
from .models import Post, Pad


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Pad)
class PadAdmin(admin.ModelAdmin):
    pass