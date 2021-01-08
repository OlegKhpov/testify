from django.forms.models import inlineformset_factory
from django.test import TestCase

from testify.forms import AnswerInlineFormSet, AnswerAdminForm, QuestionAdminForm, QuestionInlineFormSet
from testify.models import Answer, Question, Test


class TestAdminPanel(TestCase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.test = Test.objects.create(
            name='testo',
            company_name='company_1',
            description='amazing',
            )
        self.question = Question.objects.first()
        self.QuestionFormSet = inlineformset_factory(
            Test, Question, QuestionAdminForm, formset=QuestionInlineFormSet
        )
        self.questions_data = {
            'questions-MIN_NUM_FORMS': '0',
            'questions-MAX_NUM_FORMS': '1000',
            'questions-INITIAL_FORMS': '3',
            'questions-TOTAL_FORMS': '3',
            'questions-0-question': 'a',
            'questions-0-index': 1,
            'questions-1-question': 'b',
            'questions-1-index': 2,
            'questions-2-question': 'c',
            'questions-2-index': 3,
        }
        self.AnswerFormSet = inlineformset_factory(
            Question, Answer, AnswerAdminForm, formset=AnswerInlineFormSet)
        self.data = {
            'answers-MIN_NUM_FORMS': '0',
            'answers-MAX_NUM_FORMS': '1000',
            'answers-INITIAL_FORMS': '3',
            'answers-TOTAL_FORMS': '3',
            'answers-0-text': 'a',
            'answers-0-is_correct': True,
            'answers-1-text': 'b',
            'answers-1-is_correct': False,
            'answers-2-text': 'c',
            'answers-2-is_correct': False,
        }

    def test_questions_index_not_one(self):
        self.questions_data['questions-0-index'] = 4
        formset = self.QuestionFormSet(self.questions_data, instance=self.test)
        self.assertEqual(formset.is_valid(), False)

    def test_questions_index_not_unique(self):
        self.questions_data['questions-2-index'] = 2
        formset = self.QuestionFormSet(self.questions_data, instance=self.test)
        self.assertEqual(formset.is_valid(), False)

    def test_questions_index_not_in_order(self):
        self.questions_data['questions-2-index'] = 6
        formset = self.QuestionFormSet(self.questions_data, instance=self.test)
        self.assertEqual(formset.is_valid(), False)

    def test_all_answers_correct(self):
        self.data['answers-1-is_correct'] = True
        self.data['answers-2-is_correct'] = True
        formset = self.AnswerFormSet(self.data, instance=self.question)
        self.assertEqual(formset.is_valid(), False)

    def test_no_answers_correct(self):
        self.data['answers-0-is_correct'] = False
        formset = self.AnswerFormSet(self.data, instance=self.question)
        self.assertEqual(formset.is_valid(), False)
