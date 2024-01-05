from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, generics
import uuid

# from .permissions import AllowOptionsAuthentication
from ..models import  Project, DocumentType
from ..serializers import  ProjectSerializer, DocumentTypeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    
    """list all projects, or create a new project
    Args:
        APIView (_type_): _description_
    """
    
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format = None):
        user = request.user
        projects = user.project_set.all()
        serializer = ProjectSerializer(projects, many = True)
        return Response(status=200, data=serializer.data)

    def post(self, request, format = None):
        data = request.data
        data["code"] = str(uuid.uuid4()) 
        serializer = ProjectSerializer(data=data)
        if (serializer.is_valid()):
            serializer.save(user=self.request.user)
            return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
                        
class ProjectDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class DocumentList(mixins.ListModelMixin,generics.GenericAPIView):
    
    """list all Document types that neurodata work on
    Args:
        APIView (_type_): _description_
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format = None):
        documents = DocumentType.objects.all()
        serializer = DocumentTypeSerializer(documents, many = True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)