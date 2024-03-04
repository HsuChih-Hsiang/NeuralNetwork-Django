from utility.customized_response import response
from utility.error_msg import ErrorMsg, Error
from utility.customized_auth import AdminPermission, Authentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import SearchTextSerializer, TopicCreateSerializer
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


class SubtopicLayer(TopicLayer):

    def post(self, request):
        pass

    def put(self, request):
        pass

    def get(self, request):
        pass


class ModelClassLayer(TopicLayer):

    def post(self, request):
        pass

    def put(self, request):
        pass

    def get(self, request):
        pass


class ModelDetailsLayer(TopicLayer):

    def post(self, request):
        pass

    def put(self, request):
        pass

    def get(self, request):
        pass
