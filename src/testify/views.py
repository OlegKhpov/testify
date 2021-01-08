
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views import View
from django.contrib import messages

from .forms import AnswerFormSet
from .models import Question, Test, TestParticipant
from accounts.models import User
from core.models import TestBaseDetailView, TestLogic
from core.views import LoginRequiredBaseMixin

# Create your views here.


def index(request):
    return render(request, 'testify/index.html', {
        'tests': Test.objects.all(),
    })


def leaderboard(request):
    return render(request, 'testify/leaderboard.html', {
        'persons': User.objects.order_by('-rating'),
    })


class TestDetailView(TestBaseDetailView):
    model = Test
    template_name = 'testify/test.html'
    context_object_name = 'test'
    pk_url_kwarg = 'uuid'


def restart_test(request, uuid):
    TestParticipant.get_self_object_new(request, uuid).delete()
    return redirect(reverse('testify:start', args=[uuid]))


class TestRunnerView(LoginRequiredBaseMixin, View):
    def get(self, request, uuid):
        user = request.user
        state = TestParticipant.STATE.NEW
        test = Test.objects.get(uuid=uuid)
        if TestParticipant.objects.filter(user=user, state=state, test=test).count() == 0:
            TestParticipant.objects.create(
                user=user,
                state=state,
                test=test
            )
        return redirect(reverse('testify:question', args=[uuid, ]))


class QuestionView(View):
    def get(self, request, uuid):
        test_result = TestParticipant.get_self_object_new(request, uuid)
        question = Question.objects.get(test__uuid=uuid, index=test_result.current_question)
        answers = question.answers.all()
        form_set = AnswerFormSet(queryset=answers)
        return render(request, 'testify/passing.html', {
            'question': question,
            'form_set': form_set,
        })

    def post(self, request, uuid):
        forms_list = AnswerFormSet(data=request.POST).forms
        test_logic = TestLogic(TestParticipant.get_self_object_new(request, uuid))
        test_result = test_logic.get_test_result(forms_list)
        if request.user.show_result_popup:
            if test_logic.point:
                messages.success(self.request, "Well Done! That's correct!")
            else:
                messages.error(self.request, "Oops! That's wrong!")
        if test_logic.is_last():
            test_logic.actions_for_completion()
            test = test_result.test
            return render(request, 'testify/completetest.html', {
                'test_result': test_result,
                'test': test
            })

        return redirect(reverse('testify:question', args=[uuid, ]))


def error_400(request, exception):
    data = {}
    return render(request, 'testify/error_handlers/error_400.html', data)


def error_403(request, exception):
    data = {}
    return render(request, 'testify/error_handlers/error_403.html', data)


def error_404(request, exception):
    data = {}
    return render(request, 'testify/error_handlers/error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'testify/error_handlers/error_500.html', data)
