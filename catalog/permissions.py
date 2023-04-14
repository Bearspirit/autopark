from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


"""
content_type = ContentType.objects.get_for_model(Vehicles)
permission = Permission.objects.create(
    codename='can_make', 
    name='Can Make Vehicle', 
    content_type= content_type,)
"""

