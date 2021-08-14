from django.urls import path
from rest_framework.authtoken import views
from rest_framework import routers

from .views import PoolsViewSet, QuestionsViewSet, ResponseContentViewSet, AnswerCreateViewSet

router = routers.SimpleRouter()
router.register('pools', PoolsViewSet, basename='pools')
router.register('pools/(?P<pools_id>\d+)/questions', QuestionsViewSet, basename='questions')
router.register('pools/(?P<pools_id>\d+)/questions/(?P<questions_id>\d+)/response', ResponseContentViewSet,
                basename='response')
router.register('pools/(?P<pools_id>\d+)/questions/(?P<questions_id>\d+)/answer', AnswerCreateViewSet,
                basename='answer')
urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='token'),
              ] + router.urls
