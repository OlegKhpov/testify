from django.contrib import admin

from .forms import AnswerInlineFormSet, QuestionInlineFormSet
from .models import Test, Question, Answer, TestParticipant
# Register your models here.


class QuestionsTable(admin.TabularInline):
    model = Question
    fk_name = 'test'
    fields = ['question', 'index']
    read_only = fields
    show_change_link = True
    extra = 0
    formset = QuestionInlineFormSet


class AnswersTable(admin.TabularInline):
    model = Answer
    fk_name = 'question'
    fields = ['text', 'is_correct']
    extra = 0
    formset = AnswerInlineFormSet


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswersTable]


class TestAdmin(admin.ModelAdmin):
    exclude = ('uuid', 'questions_count',)
    inlines = [QuestionsTable]


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(TestParticipant)
