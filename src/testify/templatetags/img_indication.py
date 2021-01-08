import os

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def difficulty(dif):
    image_dir = os.path.join(settings.STATIC_URL, 'common/test_difficulty_indicators/')
    return os.path.join(image_dir, f'{dif}.jpg')
