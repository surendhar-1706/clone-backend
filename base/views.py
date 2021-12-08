from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from .serializers import *
from .models import *
from .pagination import *
from .filters import *


class PostListView(APIView):

    def get(self, request):
        queryset = Post.objects.all()
        paginator = CustomPaginator()
        response = paginator.generate_response(
            queryset, PostSerializer, request)
        return response

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.set_the_user(request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetriveView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostNumberforstaticpagesView(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializerStaticPage
    pagination_class = None


class PostSearch(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = PostFilter
    ordering_fields = ['date_created', 'title']

    # filterset_fields = ('title', 'skill__name')

    # search_fields = ['skill__name', 'title']
