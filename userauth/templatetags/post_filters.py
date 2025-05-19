from django import template
from userauth.models import Bookmark, LikePost

register = template.Library()

@register.filter
def is_bookmarked(post_id, username):
    """Check if a post is bookmarked by a user"""
    return Bookmark.objects.filter(post_id=post_id, user=username).exists()

@register.filter
def is_liked(post_id, username):
    """Check if a post is liked by a user"""
    return LikePost.objects.filter(post_id=post_id, username=username).exists()