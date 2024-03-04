from django.urls import path
import member.views as views


urlpatterns = [
    path('topic', views.Login.as_view()),
    path('topic/modify/<int:topic_id>', views.Login.as_view()),
]
