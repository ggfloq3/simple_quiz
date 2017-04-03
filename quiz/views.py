from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.views.generic import DetailView, FormView, TemplateView

from quiz.forms import QuestionForm
from quiz.models import Quiz, UserAnswer


class IndexView(TemplateView):
    template_name = 'quiz/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = AuthenticationForm
        context['tests'] = Quiz.objects.all()
        return context


class QuizDetail(DetailView):
    model = Quiz
    pk_url_kwarg = 'quiz_pk'
    template_name = 'quiz/quiz_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuizDetail, self).get_context_data(**kwargs)
        context['stats'] = self.object.get_stats_for_user(self.request.user)
        return context


class QuestionView(FormView):
    """
    1. в dispatch получаем следуйщий вопрос (если все вопросы отвечены - redirect на страницу с результатами)
    2. на его основе создаётся форма
    3. на основе ответа пользователя создаётся UserAnswer

    """
    form_class = QuestionForm
    template_name = 'quiz/question.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            quiz = Quiz.objects.get(pk=self.kwargs['quiz_pk'])
        except Quiz.DoesNotExist:
            raise Http404("Quiz does not exist")

        self.question = quiz.next_question_for_user(self.request.user)
        if not self.question:
            return redirect('quiz_detail', self.kwargs['quiz_pk'])
        return super(QuestionView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # передаём в форму question, для составления формы на основе question.answervariant_set
        kwargs = super(QuestionView, self).get_form_kwargs()
        kwargs['question'] = self.question
        return kwargs

    def form_valid(self, form):
        # Проверка ответа на правильность и создание UserAnswer
        user_choiced_ids = [int(x.split('_')[1]) for x in form.cleaned_data if form.cleaned_data[x]]
        right_ids = self.question.get_right_ids()
        answer_is_right = set(user_choiced_ids) == set(right_ids)
        UserAnswer.objects.create(is_right=answer_is_right, user=self.request.user, question=self.question)
        return super(QuestionView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuestionView, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz_pk'] = self.kwargs['quiz_pk']
        return context

    def get_success_url(self):
        return reverse('next_question', kwargs={'quiz_pk': self.kwargs['quiz_pk']})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('index'))
    else:
        form = UserCreationForm

    context = {'form': form}
    return render(request, 'quiz/registration.html', context)
