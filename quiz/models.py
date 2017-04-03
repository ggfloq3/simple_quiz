from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Quiz(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название теста')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def get_absolute_url(self):
        return reverse('quiz_detail', args=[self.id])

    def next_question_for_user(self, user):
        # возвращаем первый из неотвеченных вопросов
        return self.question_set.exclude(useranswer__user=user).first()

    def get_stats_for_user(self, user):
        # результаты тестирования для пользователя
        questions = self.question_set.all()
        question_count = questions.count()
        answered = questions.filter(useranswer__user=user).count()
        answered_right = questions.filter(useranswer__user=user, useranswer__is_right=True).count()
        right_percent = int(answered_right / answered * 100) if answered > 0 else 0
        completed_percent = int(answered / question_count * 100) if question_count > 0 else 0

        stats = {
            'question_count': question_count,
            'answered': answered,
            'answered_right': answered_right,
            'right_percent': right_percent,
            'completed_percent': completed_percent,
        }
        return stats


class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    title = models.CharField(max_length=255, verbose_name='Вопрос')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('order',)

    def get_absolute_url(self):
        return reverse('question_detail', args=[self.quiz_id, self.id])

    def get_right_ids(self):
        # список id правильных ответов
        return list(
            self.answervariant_set.filter(is_right=True).values_list('id', flat=True)
        )


class AnswerVariant(models.Model):
    question = models.ForeignKey(Question)
    title = models.CharField(max_length=255, verbose_name='Вариант ответа')
    is_right = models.BooleanField(verbose_name='Правильный ответ')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


class UserAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    is_right = models.BooleanField()

    class Meta:
        unique_together = ('user', 'question')
