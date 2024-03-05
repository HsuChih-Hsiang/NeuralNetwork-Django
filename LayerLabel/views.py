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
        topic = Topic.objects.filer(is_show=True)
        data = TopicCreateSerializer(topic, many=True).data
        return response(data=data)

    def get(self, request):
        search = SearchTextSerializer(data=request.query_params)
        if not search.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        search_txt = search.validated_data.get('search_txt')

        if search_txt or not search_txt.is_space():
            topic = Topic.objects.filer(is_show=True, name__contains=search_txt)
        else:
            topic = Topic.objects.filer(is_show=True)

        data = TopicCreateSerializer(topic, many=True).data
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

        topic = Topic.objects.filter(id=topic_id)
        if not topic:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters -- topic id')

        check.instance = topic
        check.save()

        topic = Topic.objects.filer(is_show=True)
        data = TopicCreateSerializer(topic, many=True).data
        return response(data=data)


class SubtopicLayer(APIView):
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
        check = SubtopicCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        check.save()
        topic = Topic.objects.filer(is_show=True)
        data = SubtopicCreateSerializer(topic, many=True).data
        return response(data=data)

    def get(self, request, subtopic_id):
        search = SearchTextSerializer(data=request.query_params)
        if not search.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        search_txt = search.validated_data.get('search_txt')

        if search_txt or not search_txt.is_space():
            subtopic = Subtopic.objects.filer(is_show=True, name__contains=search_txt, topic=subtopic_id)
        else:
            subtopic = Subtopic.objects.filer(is_show=True, topic=subtopic_id)

        data = SubtopicCreateSerializer(subtopic, many=True, context="subtopic").data
        return response(data=data)


class UpdateSubtopicLayer(APIView):
    def put(self, request, subtopic_id):
        check = SubtopicCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        subtopic = Subtopic.objects.filter(id=subtopic_id)
        if not subtopic:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters -- subtopic id')

        check.instance = subtopic
        check.save()

        return response()


class ModelClassLayer(APIView):
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
        check = ModelClassCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        check.save()
        model_class = ModelClass.objects.filer(is_show=True)
        data = ModelClassCreateSerializer(model_class, many=True).data
        return response(data=data)

    def get(self, request, model_class_id):
        search = SearchTextSerializer(data=request.query_params)
        if not search.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        search_txt = search.validated_data.get('search_txt')

        if search_txt or not search_txt.is_space():
            model_class = ModelClass.objects.filer(is_show=True, name__contains=search_txt, sub_topic=model_class_id)
        else:
            model_class = ModelClass.objects.filer(is_show=True, sub_topic=model_class_id)

        data = ModelClassCreateSerializer(model_class, many=True, context="class").data
        return response(data=data)


class UpdateModelClassLayer(APIView):
    def put(self, request, model_class_id):
        check = ModelClassCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        model_class = ModelClass.objects.filter(id=model_class_id)
        if not model_class:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters -- class id')

        check.instance = model_class
        check.save()

        model_class = ModelClass.objects.filer(is_show=True)
        data = ModelClassCreateSerializer(model_class, many=True).data
        return response(data=data)


class ModelDetailsLayer(APIView):
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
        check = ModelDetailsCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        check.save()
        model_class = ModelDetails.objects.filer(is_show=True)
        data = ModelDetailsCreateSerializer(model_class, many=True).data
        return response(data=data)

    def get(self, request, model_detail_id):
        search = SearchTextSerializer(data=request.query_params)
        if not search.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')
        search_txt = search.validated_data.get('search_txt')

        if search_txt or not search_txt.is_space():
            model_class = ModelDetails.objects.filer(
                is_show=True, name__contains=search_txt, model_class=model_detail_id
            )
        else:
            model_class = ModelDetails.objects.filer(is_show=True, model_class=model_detail_id)

        data = ModelClassCreateSerializer(model_class, many=True, context="class").data
        return response(data=data)


class UpdateModelDetailsLayer(APIView):
    def put(self, request, model_class_id):
        check = ModelDetailsCreateSerializer(data=request.data)
        if not check.is_valid():
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters')

        model_class = ModelDetails.objects.filter(id=model_class_id)
        if not model_class:
            raise Error(ErrorMsg.BAD_REQUEST, 'Bad Parameters -- model detail id')

        check.instance = model_class
        check.save()

        model_class = ModelDetails.objects.filer(is_show=True)
        data = ModelDetailsCreateSerializer(model_class, many=True).data
        return response(data=data)
