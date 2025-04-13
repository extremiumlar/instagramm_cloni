from django.contrib import admin
from .models import Posts , PostLike, PostComments, CommentLike


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'caption', 'created_at')
    search_fields = ('id', 'author__username', 'caption')
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at')
    search_fields = ('id', 'author__username', 'comment')

class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'comment', 'created_at')
    search_fields = ('id', 'author__useraname', 'comment')
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_at')
    search_fields = ('id', 'author__username')

admin.site.register(Posts, PostAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(PostComments, PostCommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)


