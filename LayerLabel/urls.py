from django.urls import path
import LayerLabel.views as views


urlpatterns = [
    path('topic', views.TopicLayer.as_view()),
    path('topic/modify/<int:topic_id>', views.UpdateTopicLayer.as_view()),

    path('subtopic', views.SubtopicLayer.as_view()),
    path('subtopic/create/<int:topic_id>', views.CreateSubtopicLayer.as_view()),
    path('subtopic/modify/<int:subtopic_id>', views.UpdateSubtopicLayer.as_view()),

    path('model_class', views.ModelClassLayer.as_view()),
    path('model_class/create/<int:subtopic_id>', views.CreateModelClassLayer.as_view()),
    path('model_class/modify/<int:model_class_id>', views.UpdateModelClassLayer.as_view()),

    path('model_detail', views.ModelDetailsLayer.as_view()),
    path('model_detail/create/<int:model_class_id>', views.CreateModelDetailsLayer.as_view()),
    path('model_detail/modify/<int:model_detail_id>', views.UpdateModelDetailsLayer.as_view()),
]
