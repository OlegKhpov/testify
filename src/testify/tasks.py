import datetime

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from core.models import Reminder

from testify.models import TestParticipant
from accounts.models import User


@shared_task
def check_test_complete_after_register(username):
    if TestParticipant.objects.filter(user__username=username).count() == 0:
        send_mail(
            subject='Welcome to Testify service!',
            message='Hi, it is time to pass some tests on our web service. Enjoy!',
            from_email=settings.EMAIL_OWNER,
            recipient_list=[User.objects.get(username=username).email],
        )


@shared_task
def check_last_days():
    SEND_LIMIT = 2  # times
    MIN_REMINDER_PERIOD_MONTHS = 3  # months
    for testresult in TestParticipant.objects.filter(state=TestParticipant.STATE.NEW):
        obj = Reminder.objects.get_or_create(
            user=testresult.user,
            test=testresult.test,
        )
        obj = obj[0]
        if timezone.now() < (obj.email_date + datetime.timedelta(days=30 * MIN_REMINDER_PERIOD_MONTHS))\
                and obj.counter < SEND_LIMIT:
            obj.send_reminder()
            obj.counter += 1
            obj.save()
