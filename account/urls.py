from django.urls import path

from account import views

# from rest_framework import routers
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('verify/', views.UserVerifyTokenView.as_view(), name='verify'),

    path('update-password/', views.UpdatePasswordView.as_view(), name='update-password'),
    path('user/<int:pk>/', views.UserRetrieveView.as_view(), name='user'),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/', views.UserListView.as_view(), name='users'),
]

# router = routers.SimpleRouter()
# router.register(r'user', views.UserViewSet, 'user')
#
# urlpatterns += router.urls
