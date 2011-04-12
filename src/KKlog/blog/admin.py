from KKlog.blog.models import Comment, Category, Post
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)
    list_display = ('title', 'published')
    prepopulated_fields = {"slug": ("title",)}
    
class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "author", "created"]

admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)