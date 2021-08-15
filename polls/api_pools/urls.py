from django.urls import path
from rest_framework.authtoken import views
from rest_framework import routers

from .views import PoolsViewSet, QuestionsViewSet, ResponseContentViewSet, AnswerCreateViewSet, UserSurveyInformation

router = routers.SimpleRouter()
router.register(r'pools', PoolsViewSet, basename='pools')
router.register(r'pools/(?P<pools_id>\d+)/questions', QuestionsViewSet, basename='questions')
router.register(r'pools/(?P<pools_id>\d+)/questions/(?P<questions_id>\d+)/response', ResponseContentViewSet,
                basename='response')
router.register(r'pools/(?P<pools_id>\d+)/questions/(?P<questions_id>\d+)/answer', AnswerCreateViewSet,
                basename='answer')
router.register(r'user', UserSurveyInformation,
                basename='user')
urlpatterns = [
                  path('api-token-auth/', views.obtain_auth_token, name='token'),

              ] + router.urls
