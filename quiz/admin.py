from django.contrib import admin

# Register your models here.
from quiz.models import Quiz, Question, AnswerVariant, UserAnswer
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline


class AnswerInline(NestedTabularInline):
    model = AnswerVariant
    extra = 0


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 0
    inlines = [AnswerInline, ]


class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionInline, ]


class UserAnswerAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    list_display = ('id', 'user', 'question', 'is_right')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)


#
# class AnswerInline(admin.TabularInline):
#     model = QuestionAnswer
#     extra = 0
#
#
# class QuiestionAdmin(admin.ModelAdmin):
#     inlines = [AnswerInline]


# admin.site.register(Question, QuiestionAdmin)
