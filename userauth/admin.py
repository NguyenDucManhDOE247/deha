from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Post, LikePost, Followers

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
    list_display = ('user', 'caption_preview', 'post_image_display', 'created_at', 'no_of_likes')
    list_filter = ('created_at',)
    search_fields = ('user', 'caption')
    
    def caption_preview(self, obj):
        return obj.caption[:50] + "..." if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Caption'
    
    def post_image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    post_image_display.short_description = 'Image'

class LikePostAdmin(admin.ModelAdmin):
    list_display = ('username', 'post_id')
    search_fields = ('username', 'post_id')
    list_filter = ('username',)

class FollowersAdmin(admin.ModelAdmin):
    list_display = ('follower', 'user')
    search_fields = ('follower', 'user')
    list_filter = ('follower', 'user')

# Register models with custom admin classes
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(Followers, FollowersAdmin)

# Fix model verbose names
admin.site.site_header = "Social Media Administration"
admin.site.site_title = "Social Media Admin Portal"
admin.site.index_title = "Welcome to Social Media Admin Portal"