from django.contrib import admin
from dryblog.models import Post, Comment
# Register your models here.

# admin.site.register(Post)
# admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('p_title','p_name','p_date')
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','c_name','c_date','c_description')
