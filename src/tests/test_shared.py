import datetime
from django.test import TestCase
from django.test.utils import override_settings
from accounts.models import User
from core.models import Reminder
from testify.models import Test, TestParticipant
from testify.tasks import check_last_days, check_test_complete_after_register


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPOGATES=True,
)
class TestBaseCase(TestCase):
    pass


class TestTasks(TestBaseCase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.user = User.objects.create(
            username='testUser',
            email='testUser@test.com',
            password='12341234Oo'
        )

    def test_morning_check(self):
        self.test = Test.objects.all().last()
        self.test_participant = TestParticipant.objects.create(
            user=self.user,
            test=self.test
        )
        task = check_last_days.apply_async(
            eta=datetime.datetime.now() + datetime.timedelta(seconds=2)
        )
        self.assertNotEqual(task.status, "SUCCESS")  # Not equal because email not going out
        reminder = Reminder.objects.get(user=self.user, test=self.test)
        reminder.email_date = datetime.datetime.now() - datetime.timedelta(days=190)
        reminder.counter = 0
        reminder.save()
        task = check_last_days.apply_async(
            eta=datetime.datetime.now() + datetime.timedelta(seconds=2)
        )
        self.assertNotEqual(task.status, "SUCCESS")  # Not equal because email not going out

    def test_user_create_task(self):
        username = self.user.username
        task = check_test_complete_after_register.s(username).delay()
        self.assertEqual(task.status, "SUCCESS")
