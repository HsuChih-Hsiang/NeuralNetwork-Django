from django.urls import path
import member.views as views


urlpatterns = [
    path('login/', views.Login),
    path('register/', views.Register),
]
