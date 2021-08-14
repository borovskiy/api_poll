from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .serializers import PoolSerializers, QuestionsSerializers, ResponseContentSerializer, \
    AnswerForManyResponsesSerializer, AnswerForTextResponsesSerializer, AnswerForOneResponsesSerializer, \
    PoolUpdateSerializers
from .models import Poll, Question, ResponseContent, Answer


class PoolsViewSet(ModelViewSet):
    """
    Вьюсет для отображения опросников:
    Просматривать могут все
    Добавлять, Изменять, Удалять только IsAdminUser
    """
    serializer_class = PoolSerializers
    queryset = Poll.objects.all()

    def get_queryset(self):
        return super().get_queryset()

    def get_permissions(self):
        if self.action in ('list', 'retrieve',):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update',):
            return PoolUpdateSerializers
        return PoolSerializers


class QuestionsViewSet(ModelViewSet):
    """
    Вьюсет для отображения опросов в опроснике:
    Просматривать могут все
    Добавлять, Изменять, Удалять только IsAdminUser
    """
    lookup_value_regex = '\d+'
    serializer_class = QuestionsSerializers
    queryset = Question.objects.all()

    def get_queryset(self):
        """Достаем queryset через related_name по id впороса"""
        poll = get_object_or_404(Poll, id=self.kwargs['pools_id'])
        return poll.questions.all()

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ResponseContentViewSet(ModelViewSet):
    """
    Вьюсет для работы с вариантами ответа к вапросу который достается из questions_id в url
    Просматривать могут все
    Добавлять, Изменять, Удалять только IsAdminUser
    """
    serializer_class = ResponseContentSerializer
    queryset = ResponseContent.objects.all()

    def perform_create(self, serializer):
        """Добавляем варианту ответа id вопроса"""
        response = get_object_or_404(Question, id=self.kwargs['questions_id'])
        serializer.save(question=response)

    def get_queryset(self):
        queryset = self.queryset.filter(question=self.kwargs['questions_id'])
        return queryset

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AnswerCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Ответ пользователя
    Список тут для того чтобы пока находишься на ответе не забыть вопрос. Сделал больше для удобства при разработке
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerForManyResponsesSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        """
        Для определения сериализатора в зависимости от типа ответа в вопросе
        """
        question = get_object_or_404(Question, pk=self.kwargs['questions_id'], )
        # Меняет сериализатор для запроса list(GET)
        if self.action in ['list']:
            return QuestionsSerializers
        if question.type_question == 'text_field':
            return AnswerForTextResponsesSerializer
        elif question.type_question == 'radio':
            return AnswerForOneResponsesSerializer
        else:
            return AnswerForManyResponsesSerializer

    def get_queryset(self):
        """Которая вызывает другой queryset если метод запроса list(GET)"""
        if self.action in ['list']:
            return Question.objects.filter(id=self.kwargs['questions_id'])
        return super(AnswerCreateViewSet, self).get_queryset()

    def perform_create(self, serializer):
        """
        Создания. Проверяет какой пользователь отвечает на вопрос
        И был ли уже ответ на вопрос от пользователя
        """
        question = get_object_or_404(Question, pk=self.kwargs['questions_id'], )
        try:
            user_id = self.request.data['id_user']
            user, status = User.objects.get_or_create(username=user_id)
            if self.request.user.is_authenticated:
                user = self.request.user.id
            if len(Answer.objects.filter(question=question,author__username=user_id)) > 0:
                raise ValidationError('You have already answered this question')
            serializer.save(author_id=user.id, question=question)
        except MultiValueDictKeyError:
            raise ValidationError('You are not logged in or did not provide your id')
