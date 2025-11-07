from django.urls import path
from user.views import create_user, login

app_name = 'user'

urlpatterns = [
    path('', create_user),
    path('/login', login),
]
