from django.core.management.base import BaseCommand
from api_pools.models import Poll, Question, ResponseContent
from faker import Faker
import random


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        list_response = ['Ответ 1', 'Ответ 2', 'Ответ 3']
        list_type_questions = ['text_field', 'radio', 'check_boxes']
        fake = Faker()
        # fake.date()
        for pools in range(21):
            start_date = fake.date_this_year()
            end_date = fake.date_between(start_date=start_date, end_date='+1y')
            Poll.objects.create(title=f'Опрос {pools}', start_date=start_date, end_date=end_date,
                                description=fake.text(max_nb_chars=100))

        for pool in Poll.objects.all():
            for i in range(21):
                Question.objects.create(text=fake.text(max_nb_chars=50),
                                        type_question=random.choice(list_type_questions), poll=pool)

        for question in Question.objects.select_related('poll').all():
            if question.type_question != 'text_field':
                for resp in list_response:
                    ResponseContent.objects.create(option=resp, question=question)
