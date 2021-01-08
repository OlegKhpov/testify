import datetime as dt

from django.db import models
from django.shortcuts import get_object_or_404

from accounts.models import User
from core.utils import generate_uuid
# Create your models here.


class Test(models.Model):
    class DIFFICULTY(models.IntegerChoices):
        VERY_EASY = 1, 'Very easy',
        EASY = 2, 'Easy',
        MEDIUM = 3, 'Medium',
        HARD = 4, 'HARD',
        VERY_HARD = 5, 'Very hard'
    uuid = models.UUIDField(default=generate_uuid)
    name = models.CharField(max_length=64)
    company_name = models.CharField(max_length=64)
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=512)
    difficulty = models.PositiveIntegerField(default=DIFFICULTY.VERY_EASY)
    best_result = models.ForeignKey(to=User, on_delete=models.SET_NULL, primary_key=False, null=True)
    last_run = models.DateTimeField(null=True)

    @property
    def questions_count(self):
        return self.questions.count()

    def reward(self):
        return self.questions_count * self.difficulty

    def __str__(self):
        return f'{self.name} - {self.questions_count}'


class Question(models.Model):
    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField(max_length=1280)
    index = models.IntegerField(default=1)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=1280)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class TestParticipant(models.Model):
    class STATE(models.IntegerChoices):
        NEW = 0, 'New',
        COMPLETE = 1, "Completed"
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, related_name='participation')
    state = models.PositiveIntegerField(default=STATE.NEW, choices=STATE.choices)
    date_started = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    num_correct_ans = models.PositiveIntegerField(default=0)
    num_incorrect_ans = models.PositiveIntegerField(default=0)
    is_passed = models.BooleanField(default=False)
    date_complete = models.DateTimeField(null=True, blank=True)
    current_question = models.IntegerField(default=1)

    def compute_finals(self):
        self.state = TestParticipant.STATE.COMPLETE
        self.date_complete = self.write_date
        self.time_spent = self.date_complete - self.date_started
        if self.points() > 0:
            self.is_passed = True
        self.save()

    def points(self):
        return max(0, self.num_correct_ans - self.num_incorrect_ans)

    def time_spent(self):
        time = self.write_date - self.date_started
        return time - dt.timedelta(microseconds=time.microseconds)

    @classmethod
    def get_self_object_new(cls, request, uuid):
        return get_object_or_404(
            klass=cls,
            user=request.user,
            state=cls.STATE.NEW,
            test__uuid=uuid,
        )

    @classmethod
    def get_self_object_complete(cls, request, uuid):
        return get_object_or_404(
            klass=cls,
            user=request.user,
            state=cls.STATE.COMPLETE,
            test__uuid=uuid,
        )

    def __str__(self):
        return f'{self.test.name} - {self.user.username}'
