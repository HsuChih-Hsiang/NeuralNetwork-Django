from utility.customized_response import response
from utility.error_msg import ErrorMsg, Error
from utility.customized_auth import AdminPermission, Authentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import (SearchTextSerializer, TopicCreateSerializer, SubtopicCreateSerializer,
                          ModelClassCreateSerializer, ModelDetailsCreateSerializer)
from .models import Topic, Subtopic, ModelClass, ModelDetails


class TopicLayer(APIView):
    parser_classes = (JSONParser,)

    def get_authenticators(self):
        if self.request.method == 'POST':
            return (Authentication(),)
        return ()

    def get_permissions(self):
        if self.request.method == 'POST':
            return (AdminPermission(),)
        return ()

    def post(self, request):
        check = TopicCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        check.save()
        topic = Topic.objects.filter(is_show=True).order_by('id')
        data = TopicCreateSerializer(topic, many=True, context='topic').data
        return response(data=data)

    def get(self, request):
        search = SearchTextSerializer(data=request.query_params)
        if not search.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        search_txt = search.validated_data.get('search_txt', str())

        if search_txt and not search_txt.isspace():
            topic = Topic.objects.filter(is_show=True, name__contains=search_txt).order_by('id')
        else:
            topic = Topic.objects.filter(is_show=True).order_by('id')

        data = TopicCreateSerializer(topic, many=True, context='topic').data
        return response(data=data)


class UpdateTopicLayer(APIView):
    parser_classes = (JSONParser,)

    def get_authenticators(self):
        if self.request.method == 'PUT':
            return (Authentication(),)
        return ()

    def get_permissions(self):
        if self.request.method == 'PUT':
            return (AdminPermission(),)
        return ()

    def put(self, request, topic_id):
        check = TopicCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        topic = Topic.objects.filter(id=topic_id).first()
        if not topic:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters -- topic id')

        check.instance = topic
        check.save()

        topic = Topic.objects.filter(is_show=True).order_by('id')
        data = TopicCreateSerializer(topic, many=True, context='topic').data
        return response(data=data)


class SubtopicLayer(APIView):
    parser_classes = (JSONParser,)

    def get_authenticators(self):
        if self.request.method in ['POST', 'PUT']:
            return (Authentication(),)
        return ()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return (AdminPermission(),)
        return ()

    def post(self, request, subtopic_id):
        check = SubtopicCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        topic = Topic.objects.filter(id=subtopic_id).first()
        if not topic:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        check.validated_data.update({'topic_id': topic.id})

        check.save()
        topic = Subtopic.objects.filter(is_show=True).order_by('id')
        data = SubtopicCreateSerializer(topic, many=True, context="subtopic").data
        return response(data=data)

    def get(self, request, subtopic_id):
        search = SearchTextSerializer(data=request.query_params)
        if not search.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        search_txt = search.validated_data.get('search_txt', str())

        if search_txt or not search_txt.isspace():
            subtopic = Subtopic.objects.filter(is_show=True, name__contains=search_txt, topic=subtopic_id).order_by('id')
        else:
            subtopic = Subtopic.objects.filter(is_show=True, topic=subtopic_id).order_by('id')

        data = SubtopicCreateSerializer(subtopic, many=True, context="subtopic").data
        return response(data=data)

    def put(self, request, subtopic_id):
        check = SubtopicCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        subtopic = Subtopic.objects.filter(id=subtopic_id).first()
        if not subtopic:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters -- subtopic id')

        check.instance = subtopic
        check.save()

        subtopic = Subtopic.objects.filter(is_show=True).order_by('id')
        data = SubtopicCreateSerializer(subtopic, many=True, context='topic').data
        return response(data=data)


class ModelClassLayer(APIView):
    parser_classes = (JSONParser,)

    def get_authenticators(self):
        if self.request.method in ['POST', 'PUT']:
            return (Authentication(),)
        return ()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return (AdminPermission(),)
        return ()

    def post(self, request, model_class_id):
        check = ModelClassCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        subtopic = Subtopic.objects.filter(id=model_class_id).first()
        if not subtopic:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        check.validated_data.update({'sub_topic_id': subtopic.id})

        check.save()
        model_class = ModelClass.objects.filter(is_show=True).order_by('id')
        data = ModelClassCreateSerializer(model_class, many=True, context="class").data
        return response(data=data)

    def get(self, request, model_class_id):
        search = SearchTextSerializer(data=request.query_params)
        if not search.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        search_txt = search.validated_data.get('search_txt', str())

        if search_txt and not search_txt.isspace():
            model_class = ModelClass.objects.filter(
                is_show=True, name__contains=search_txt, sub_topic=model_class_id
            ).order_by('id')

        else:
            model_class = ModelClass.objects.filter(is_show=True, sub_topic=model_class_id).order_by('id')

        data = ModelClassCreateSerializer(model_class, many=True, context="class").data
        return response(data=data)

    def put(self, request, model_class_id):
        check = ModelClassCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        model_class = ModelClass.objects.filter(id=model_class_id).first()
        if not model_class:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters -- class id')

        check.instance = model_class
        check.save()

        model_class = ModelClass.objects.filter(is_show=True).order_by('id')
        data = ModelClassCreateSerializer(model_class, many=True, context="class").data
        return response(data=data)


class ModelDetailsLayer(APIView):
    parser_classes = (JSONParser,)

    def get_authenticators(self):
        if self.request.method in ['POST', 'PUT']:
            return (Authentication(),)
        return ()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return (AdminPermission(),)
        return ()

    def post(self, request, model_detail_id):
        check = ModelDetailsCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        model_class = ModelClass.objects.filter(id=model_detail_id).first()
        if not model_class:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        check.validated_data.update({'model_class_id': model_class.id})

        check.save()
        model_class = ModelDetails.objects.filter(is_show=True).order_by('id')
        data = ModelDetailsCreateSerializer(model_class, many=True, context="detail").data
        return response(data=data)

    def get(self, request, model_detail_id):
        search = SearchTextSerializer(data=request.query_params)
        if not search.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        search_txt = search.validated_data.get('search_txt', str())

        if search_txt and not search_txt.isspace():
            model_class = ModelDetails.objects.filter(
                is_show=True, name__contains=search_txt, model_class=model_detail_id
            ).order_by('id')
        else:
            model_class = ModelDetails.objects.filter(is_show=True, model_class=model_detail_id).order_by('id')

        data = ModelClassCreateSerializer(model_class, many=True, context="detail").data
        return response(data=data)

    def put(self, request, model_detail_id):
        check = ModelDetailsCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        model_class = ModelDetails.objects.filter(id=model_detail_id).first()
        if not model_class:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters -- model detail id')

        check.instance = model_class
        check.save()

        model_class = ModelDetails.objects.filter(is_show=True).order_by('id')
        data = ModelDetailsCreateSerializer(model_class, many=True, context="detail").data
        return response(data=data)

