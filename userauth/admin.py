from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Post, LikePost, Followers, Comment, Tag, Bookmark

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'profile_image_display', 'id_user')
    search_fields = ('user__username', 'location', 'bio')
    list_filter = ('location',)
    
    def profile_image_display(self, obj):
        if obj.profileimg:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profileimg.url)
        return "No Image"
    profile_image_display.short_description = 'Profile Image'

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption_preview', 'post_image_display', 'created_at', 'no_of_likes', 'tag_list')
    list_filter = ('created_at', 'tags')
    search_fields = ('user', 'caption')
    filter_horizontal = ('tags',)
    
    def caption_preview(self, obj):
        return obj.caption[:50] + "..." if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Caption'
    
    def post_image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    post_image_display.short_description = 'Image'
    
    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tag_list.short_description = 'Tags'

class LikePostAdmin(admin.ModelAdmin):
    list_display = ('username', 'post_id')
    search_fields = ('username', 'post_id')
    list_filter = ('username',)

class FollowersAdmin(admin.ModelAdmin):
    list_display = ('follower', 'user')
    search_fields = ('follower', 'user')
    list_filter = ('follower', 'user')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text_preview', 'post_link', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user', 'text', 'post__id')
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'
    
    def post_link(self, obj):
        return format_html('<a href="/admin/userauth/post/{}">{}</a>', obj.post.id, obj.post.id)
    post_link.short_description = 'Post'

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    search_fields = ('name',)
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_link', 'created_at')
    search_fields = ('user', 'post__id')
    list_filter = ('created_at',)
    
    def post_link(self, obj):
        return format_html('<a href="/admin/userauth/post/{}">{}</a>', obj.post.id, obj.post.id)
    post_link.short_description = 'Post'

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(Followers, FollowersAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Bookmark, BookmarkAdmin)

admin.site.site_header = "Social Media Administration"
admin.site.site_title = "Social Media Admin Portal"
admin.site.index_title = "Welcome to Social Media Admin Portal"