from django.urls import path
from rest_framework import routers

# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from account import views

urlpatterns = [
    path('register/', views.UserRegisterAPI.as_view(), name='register'),
    path('login/', views.ObtainJWTView.as_view(), name='login'),
    path('update-password/', views.UpdatePasswordAPI.as_view(), name='update-password'),
    path('user/<int:pk>/', views.ViewUpdateUserAPI.as_view(), name='user'),
    # path('refresh/', refresh_jwt_token, name='refresh'),
    # path('verify/', verify_jwt_token, name='verify'),
]

router = routers.SimpleRouter()
# router.register(r'user', views.UserViewSet, 'user')

urlpatterns += router.urls
