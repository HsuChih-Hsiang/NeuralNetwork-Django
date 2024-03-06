from django.urls import path
import LayerLabel.views as views


urlpatterns = [
    path('topic', views.TopicLayer.as_view()),
    path('topic/modify/<int:topic_id>', views.UpdateTopicLayer.as_view()),
    path('subtopic/<int:subtopic_id>', views.SubtopicLayer.as_view()),
    path('model_class/<int:model_class_id>', views.ModelClassLayer.as_view()),
    path('model_detail/<int:model_detail_id>', views.ModelDetailsLayer.as_view()),
]
