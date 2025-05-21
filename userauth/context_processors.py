from .models import Tag
from django.db import models

def tag_list(request):
    """
    Context processor to add tag_list to all templates - including all tags
    """
    return {
        'tag_list': Tag.objects.all().order_by('name')
    }