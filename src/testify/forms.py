from django.core.exceptions import ValidationError
from django.forms import fields
from django.forms.models import BaseInlineFormSet, modelformset_factory
from django import forms

from testify.models import Answer, Question


class AnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        num_correct_answers = sum([
            1
            for form in self.forms
            if form.cleaned_data['is_correct']
        ])

        if num_correct_answers == 0:
            raise ValidationError('At LEAST one answer must be correct!')

        if num_correct_answers == len(self.forms):
            raise ValidationError('ALL answers must not be CORRECT')


class QuestionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        indexes = []
        for form in self.forms:
            ind = form.cleaned_data['index']
            if ind in indexes:
                raise ValidationError('INDEX must be UNIQUE')
            indexes.append(ind)
        indexes.sort()
        for item in indexes:
            if item == indexes[0]:
                continue
            elif (item - 1) not in indexes:
                raise ValidationError('Indexes of the QUESTIONS must be in order!')
        if indexes[0] != 1:
            raise ValidationError('Index of the FIRST QUESTION must be 1!')


class AnswerForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False)
    test = fields.CharField()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['text'].label = ''
        self.fields['is_selected'].label = ''

    class Meta:
        model = Answer
        fields = ['text', 'is_selected']
        widgets = {
            'question': forms.TextInput(attrs={'readonly': True})
        }


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerAdminForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'


AnswerFormSet = modelformset_factory(
    model=Answer,
    form=AnswerForm,
    extra=0,
)
