from django.contrib import admin

# Register your models here.
from testsuite.forms import TestForm, QuestionsInlineFormSet, QuestionsInlineForm, VariantsInlineFormSet
from testsuite.models import Test, Question, Variant, TestResult


class QuestionsInline(admin.TabularInline):
    model = Question
    fields = ('text', 'number')  # 'num_variant_min_limit')
    show_change_link = True  # we can edit
    # extra = 1
    extra = 0  # we can add question
    formset = QuestionsInlineFormSet  # !!! set
    form = QuestionsInlineForm


class TestAdminModel(admin.ModelAdmin):
    fields = ('title', 'description', 'level', 'image')
    list_display = ('title', 'description', 'level', 'image')
    list_per_page = 10
    inlines = (QuestionsInline,)
    form = TestForm


class VariantsInline(admin.TabularInline):
    model = Variant
    fields = ('text', 'is_correct')  # 'num_variant_min_limit')
    show_change_link = False
    extra = 0
    formset = VariantsInlineFormSet


class QuestionAdminModel(admin.ModelAdmin):
    # model = Question  # can without model
    fields = ('test', 'number', 'text', 'description')  # 'num_variant_min_limit')
    list_display = ('number', 'text', 'description', 'test')
    list_per_page = 10
    list_select_related = ('test',)
    search_fields = ('text',)
    show_change_link = True
    inlines = (VariantsInline,)


admin.site.register(Test, TestAdminModel)
admin.site.register(Question, QuestionAdminModel)
admin.site.register(Variant)
admin.site.register(TestResult)
