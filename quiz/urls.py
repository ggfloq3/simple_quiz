from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from quiz.views import QuizDetail, QuestionView, IndexView, register

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^registration/$', register, name='registration'),
    url(r'^login/$', auth_views.login, {'template_name': 'quiz/index.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^quiz/(?P<quiz_pk>[^/]+)/$', login_required(QuizDetail.as_view()), name='quiz_detail'),
    url(r'^quiz/(?P<quiz_pk>[^/]+)/question/$', login_required(QuestionView.as_view()), name='next_question'),
]
