import datetime

from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import mixins, viewsets, generics, exceptions, permissions

from .serializers import PoolSerializers, QuestionsSerializers, ResponseContentSerializer, \
    AnswerForManyResponsesSerializer, AnswerForTextResponsesSerializer, AnswerForOneResponsesSerializer, \
    PoolUpdateSerializers, UserSerializer
from .models import Poll, Question, ResponseContent, Answer


class PoolsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отображения опросников:
    Просматривать могут все
    Добавлять, Изменять, Удалять только IsAdminUser
    """
    serializer_class = PoolSerializers
    queryset = Poll.objects.filter(end_date__gte=datetime.datetime.now())

    def get_queryset(self):
        if self.request.user.is_staff:
            return Poll.objects.all()
        return super().get_queryset()

    def get_permissions(self):
        if self.action in ('list', 'retrieve',):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update',):
            return PoolUpdateSerializers
        return PoolSerializers


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отображения опросов в опроснике:
    Просматривать могут все
    Добавлять, Изменять, Удалять только IsAdminUser
    """
    serializer_class = QuestionsSerializers
    queryset = Question.objects.select_related('poll').filter(poll__end_date__gte=datetime.datetime.now())

    def get_queryset(self):
        """Достаем queryset через related_name по id впороса"""
        if self.request.user.is_staff:
            return Question.objects.select_related('poll').all()
        return Question.objects.select_related('poll').filter(poll__end_date__gte=datetime.datetime.now(),
                                                              poll_id=self.kwargs['pools_id'])

    def perform_create(self, serializer):
        response = generics.get_object_or_404(Poll, id=self.kwargs['pools_id'])
        serializer.save(poll=response)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class ResponseContentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с вариантами ответа к вапросу который достается из questions_id в url
    Просматривать могут все
    Добавлять, Изменять, Удалять только IsAdminUser
    """
    serializer_class = ResponseContentSerializer
    queryset = ResponseContent.objects.all()

    def perform_create(self, serializer):
        """Добавляем варианту ответа id вопроса"""
        response = generics.get_object_or_404(Question, id=self.kwargs['questions_id'])
        serializer.save(question=response)

    def get_queryset(self):
        return ResponseContent.objects.select_related('question').filter(
            question__poll__end_date__gte=datetime.datetime.now(), question=self.kwargs['questions_id'])

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class AnswerCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Ответ пользователя
    Список тут для того чтобы пока находишься на ответе не забыть вопрос. Сделал больше для удобства при разработке
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerForManyResponsesSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        """
        Для определения сериализатора в зависимости от типа ответа в вопросе
        """
        question = generics.get_object_or_404(Question, pk=self.kwargs['questions_id'], )
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
        question = generics.get_object_or_404(Question, pk=self.kwargs['questions_id'], )
        try:
            if self.request.user.is_authenticated:
                user = self.request.user
            else:
                user = self.request.data['id_user']
                user, status = User.objects.get_or_create(username=user)
            if len(Answer.objects.filter(author_id=user.id, question=question)) > 0:
                raise exceptions.ValidationError('You have already answered this question')
            serializer.save(author_id=user.id, question=question)
        except MultiValueDictKeyError:
            raise exceptions.ValidationError('You are not logged in or did not provide your "id_user" ')


class UserSurveyInformation(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Просмотр пользователя с его ответами"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Просто поставил админа т.к. небыло конкретных условий кто может просматривать
    permission_classes = [permissions.IsAdminUser]
