from django.contrib import admin
from django.urls import path
from .views import CustomAuthToken #,ListUsers



urlpatterns = [
    path('token/auth/', CustomAuthToken.as_view()),
    # path('account/users/', ListUsers.as_view()),
]
