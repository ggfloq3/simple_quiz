from django import forms
from django.core.exceptions import ValidationError


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        # формируем форму на основе вариантов ответов.
        for x in question.answervariant_set.all():
            name = 'question_{}'.format(x.id)
            self.fields[name] = forms.BooleanField(label=x.title, required=False)
        print(self.fields)

    def clean(self):
        # Если пользователь не выбрал ни одного варианта, то ValidationError
        if any(self.cleaned_data.values()):
            return super(QuestionForm, self).clean()
        else:
            raise ValidationError('Выберите хотя бы один вариант')
