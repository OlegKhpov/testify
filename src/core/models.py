from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.views.generic.detail import DetailView
from accounts.models import User # noqa

from testify.models import Question, Test, TestParticipant
# Create your models here.


class TestBaseDetailView(DetailView):
    def get_object(self):
        uuid = self.kwargs.get('uuid')
        return self.get_queryset().get(uuid=uuid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fltr = TestParticipant.objects.filter(
            user=self.request.user,
            state=TestParticipant.STATE.NEW,
            test=self.get_object(),
        )
        context['results'] = TestParticipant.objects.filter(
            user=self.request.user,
            state=TestParticipant.STATE.COMPLETE,
            test=self.get_object(),
            is_passed=True,
        )
        context['continue'] = fltr.count()
        if fltr.count():
            context['current_started'] = fltr.first()
        return context


class TestLogic:
    def __init__(self, obj):
        self.obj = obj
        self.uuid = self.obj.test.uuid
        self.index = self.obj.current_question
        self.question = Question.objects.get(test__uuid=self.uuid, index=self.index)

    def is_last(self):
        if self.index == self.question.test.questions_count:
            return True
        else:
            return False

    def get_test_result(self, forms_list):
        self.answers = self.question.answers.all()

        possible_choices = len(forms_list)
        selected_choices = [
            'is_selected' in form.changed_data
            for form in forms_list
        ]

        correct_choices = sum(
            answer.is_correct == choice
            for answer, choice in zip(self.answers, selected_choices)
        )

        self.point = int(correct_choices == possible_choices)
        self.obj.num_correct_ans += self.point
        self.obj.num_incorrect_ans += (1 - self.point)
        self.obj.current_question = self.index+1
        self.obj.save()
        self.test_result = self.obj
        return self.test_result

    def actions_for_completion(self):
        self.test_result.current_question = self.index
        self.test_result.compute_finals()

        test = self.test_result.test
        test_leader = TestParticipant.objects.filter(test__uuid=self.uuid).extra(select={
            'points': 'num_correct_ans - num_incorrect_ans',
            'time_spent': 'write_date - date_started',
            },
            order_by=['-points', 'time_spent']).first() # noqa
        test.best_result = test_leader.user
        test.last_run = self.test_result.write_date
        test.save()


class Reminder(models.Model):
    TIMES_TO_REMIND = 2
    PERIOD_TO_REMIND_MONTHS = 3
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    email_date = models.DateTimeField(auto_now=True)
    counter = models.IntegerField(default=0)

    @classmethod
    def send_reminder(cls):
        send_mail(
            subject=f'Hello, {cls.user.username}. This is Reminder from Testify service!',
            message=f'Our team would like to remind you that you have {cls.test.name} not completed yet.\
                Please, visit our service to make it done :)',
            from_email=settings.EMAIL_OWNER,
            recipient_list=[cls.user.objects.get(username=cls.user.username).email, ],
        )
        cls.save()
