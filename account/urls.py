from django.urls import path
from rest_framework import routers

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from account import views

urlpatterns = [
    path('register/', views.UserRegisterAPI.as_view(), name='register'),
    path('login/', obtain_jwt_token, name='login'),
    path('refresh/', refresh_jwt_token, name='refresh'),
    path('verify/', verify_jwt_token, name='verify'),
]

router = routers.SimpleRouter()
router.register(r'user_view', views.UserViewSet, 'user_view')

urlpatterns += router.urls
