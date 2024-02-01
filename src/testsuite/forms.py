from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from testsuite.models import Test, Question


class TestForm(ModelForm):
    model = Test

    class Meta:
        fields = '__all__'

    def clean(self):
        pass


class QuestionForm(ModelForm):
    model = Question

    class Meta:
        fields = '__all__'

    def clean(self):
        pass


class QuestionsInlineFormSet(BaseInlineFormSet):
    # instance ---> this is object Test, forms ---> questions set !!!
    def clean(self):
        if not (self.instance.MIN_LIMIT <= len(self.forms) <= self.instance.MAX_LIMIT):
            raise ValidationError('Quantity of questions is out of range ({}..{})'.format(
                self.instance.MIN_LIMIT, self.instance.MAX_LIMIT
            ))


class QuestionsInlineForm(ModelForm):

    def clean(self):
        pass


class VariantsInlineFormSet(BaseInlineFormSet):

    def clean(self):
        if not (self.instance.MIN_LIMIT <= len(self.forms) <= self.instance.MAX_LIMIT):
            raise ValidationError('Quantity of variants is out of range ({}..{})'.format(
                self.instance.MIN_LIMIT, self.instance.MAX_LIMIT
            ))

        correct_list = [
            form.cleaned_data['is_correct']
            for form in self.forms
        ]

        if not any(correct_list):
            raise ValidationError('You should select AT LEAST one correct variant!')

        if all(correct_list):
            raise ValidationError('You should NOT select ALL correct variants!')
