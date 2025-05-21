from .models import Tag
from django.db import models

def tag_list(request):
    return {
        'tag_list': Tag.objects.all().order_by('name')
    }