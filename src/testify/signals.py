from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import TestParticipant


@receiver(post_save, sender=TestParticipant)
def add_rating(sender, instance, **kwargs):
    if instance.is_passed:
        reward = instance.points()
        instance.user.add_points_to_rating(reward)
