from django.contrib.auth.models import AbstractUser
from django.db import models

from core.utils import generate_uuid
# Create your models here.


class User(AbstractUser):
    uuid = models.UUIDField(default=generate_uuid)
    bio = models.TextField(max_length=512, blank=True)
    location = models.CharField(max_length=64, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_img = models.ImageField(null=True, default='default.jpeg', upload_to='profile_imgs')
    rating = models.PositiveIntegerField(default=0)
    show_result_popup = models.BooleanField(default=False)

    def add_points_to_rating(self, test_reward):
        self.rating += test_reward
        self.save(update_fields=['rating'])

    def __str__(self):
        return self.username
