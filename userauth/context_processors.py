from .models import Tag
from django.db import models

def tag_list(request):
    """
    Context processor to add tag_list to all templates - filtered to only include tags with posts
    """
    return {
        'tag_list': Tag.objects.annotate(post_count=models.Count('posts')).filter(post_count__gt=0).order_by('name')
    }