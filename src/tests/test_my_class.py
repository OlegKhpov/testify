from django.test import TestCase
from django.test import Client
from django.urls import reverse

from testify.models import Test


class TestifyTest(TestCase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]
    TEST_OBJ = Test.objects.all().last()

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='admin')

    def test_success_flow(self):
        response = self.client.get(reverse('testify:start', kwargs={'uuid': self.TEST_OBJ.uuid}))
        self.assertRedirects(response, reverse('testify:question', kwargs={'uuid': self.TEST_OBJ.uuid}))

        questions_count = self.TEST_OBJ.questions_count

        for step in range(1, questions_count+1):
            next_url = reverse('testify:question', kwargs={'uuid': self.TEST_OBJ.uuid})
            response = self.client.get(next_url)
            self.assertEqual(response.status_code, 200)

            curr_questions_answers = self.TEST_OBJ.questions.get(index=step).answers.all()
            forms_count = len(curr_questions_answers)
            response_data = {
                'form-TOTAL_FORMS': f'{forms_count}',
                'form-INITIAL_FORMS': f'{forms_count}',
                'form-MIN_NUM_FORMS': '0',
                'form-MAX_NUM_FORMS': '1000',
            }
            for num, ans in enumerate(curr_questions_answers):
                if ans.is_correct:
                    response_data[f'form-{num}-is_selected'] = 'on'

            response = self.client.post(
                path=next_url,
                data=response_data,
            )
            if step < questions_count:
                self.assertRedirects(response, next_url)
            else:
                self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Congratulations!')
