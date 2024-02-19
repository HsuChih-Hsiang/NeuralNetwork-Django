from django.urls import path
import member.views as views


urlpatterns = [
    path('login', views.Login.as_view()),
    path('register', views.Register.as_view()),
]
