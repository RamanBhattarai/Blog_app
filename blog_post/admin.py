from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')  # Columns shown in list view
    search_fields = ('title', 'content')  # Search box
    list_filter = ('author', 'created_at')  # Right-side filters
    ordering = ('-updated_at',)
