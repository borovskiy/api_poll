from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Poll(models.Model):
    """Модель Опроса"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    start_date = models.DateField(verbose_name='Дата начала опроса')
    end_date = models.DateField(verbose_name='Дата окончания опроса')
    description = models.CharField(max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.title


TYPES_QUESTION = (
    ('text_field', 'Ответ текстом'),
    ('radio', 'Один вариант'),
    ('check_boxes', 'Выбор нескольких вариантов'),
)


class Question(models.Model):
    """Модель вопроса"""
    text = models.TextField(verbose_name='Текст вопроса')
    type_question = models.CharField(max_length=20, verbose_name='Тип вопроса', choices=TYPES_QUESTION, )
    poll = models.ForeignKey(Poll, blank=True, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        # Без такого в админке запутаться можно
        return f'{self.text}-{self.type_question}-{self.poll}'


class ResponseContent(models.Model):
    """Модель ответа для вопроса"""
    option = models.TextField(verbose_name='Вариант ответа')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")

    def __str__(self):
        return f'{self.option}-{self.question}'


class Answer(models.Model):
    """Модель ответа пользователя"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    many_response = models.ManyToManyField(ResponseContent)
    one_response = models.ForeignKey(ResponseContent, null=True, on_delete=models.CASCADE,
                                     related_name="answers_one_choice")
    self_response = models.TextField(null=True)
