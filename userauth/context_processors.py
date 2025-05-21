from .models import Tag
from django.db.models import Count

def tag_list(request):
    all_tags = Tag.objects.all().order_by('name')
    
    tags_with_posts = Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('name')
    
    return {
        'tag_list': all_tags,  
        'tags_with_posts': tags_with_posts  
    }