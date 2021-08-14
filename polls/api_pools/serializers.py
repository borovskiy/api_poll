from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Poll, Question, Answer, ResponseContent


class PoolSerializers(serializers.ModelSerializer):
    """Сериализатор для опросов"""

    class Meta:
        model = Poll
        fields = ['id', 'title', 'start_date', 'end_date', 'description']

class PoolUpdateSerializers(serializers.ModelSerializer):
    """Сериализатор для опросов"""

    class Meta:
        model = Poll
        fields = ['id', 'title', 'end_date', 'description']


class ResponseContentSerializer(serializers.ModelSerializer):
    """Сериализатор для ответов к вопросу"""

    class Meta:
        fields = ['id', 'option']
        model = ResponseContent


class QuestionsSerializers(serializers.ModelSerializer):
    """Сериализатор для вопросов к опроснику"""
    responses = ResponseContentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type_question', 'poll', 'responses']


class AnswerForManyResponsesSerializer(serializers.ModelSerializer):
    """Серализатор для ответа с множеством вариантов"""
    many_response = PrimaryKeyRelatedField(many=True, write_only=True, queryset=ResponseContent.objects.all())

    class Meta:
        fields = ['many_response']
        model = Answer

    def create(self, validated_data):
        # Проверяет принадлежат ли варианты ответов текущему вопросу
        data = [obj.id for obj in validated_data['many_response']]
        responses = validated_data['question'].responses.select_related('question').all()
        if set(data).issubset(set(responses.values_list('id', flat=True))):
            return super().create(validated_data)
        raise ValidationError('options are incorrect')


class AnswerForOneResponsesSerializer(serializers.ModelSerializer):
    """Серализатор для ответа с одним ответом"""
    one_response = PrimaryKeyRelatedField(queryset=ResponseContent.objects.all())

    class Meta:
        fields = ['one_response']
        model = Answer

    def create(self, validated_data):
        # Проверяет принадлежат ли варианты ответов текущему вопросу.
        # Можно было бы запилить отдельный сервис для проверки но ради 2 повторени мне показалось не стоит
        responses = validated_data['question'].responses.select_related('question').all()
        if validated_data['one_response'].id in responses.values_list('id', flat=True):
            return super().create(validated_data)
        raise ValidationError('Incorrect data')


class AnswerForTextResponsesSerializer(serializers.ModelSerializer):
    """Серализатор для ответа текстом"""

    class Meta:
        fields = ['self_response']
        model = Answer
