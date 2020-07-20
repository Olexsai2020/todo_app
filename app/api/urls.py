from django.urls import path
from django.conf.urls import include
from rest_framework import routers

from .views import UserSignupView, UserLoginView, TodoViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('todo', TodoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/signup', UserSignupView.as_view(), name='signup'),
    path('user/login', UserLoginView.as_view(), name='login'),
]
