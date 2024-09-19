from django.contrib import admin
from .models import Post, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created_at')
    list_filter = ('post', 'author', 'created_at')
    search_fields = ('text',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'created_at', 'likes_count')
    list_filter = ('author', 'created_at')
    search_fields = ('text',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)