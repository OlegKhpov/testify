import datetime as dt

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User
from testify.tasks import check_test_complete_after_register


@receiver(post_save, sender=User)
def start_countdown(sender, instance, **kwargs):
    username = instance.username
    check_test_complete_after_register.apply_async(
        kwargs={"username": username},
        eta=dt.datetime.now() + dt.timedelta(seconds=5)
        )
