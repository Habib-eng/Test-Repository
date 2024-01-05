from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
# from .permissions import AllowOptionsAuthentication
from .models import  Project
from apps.core.serializers import  ProjectSerializer
from django.http import Http404
from .services.storage import upload_file_to_s3

from django.contrib.auth import get_user_model
User = get_user_model()

class ProjectList(APIView):
    
    """list all projects, or create a new project
    Args:
        APIView (_type_): _description_
    """
    
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request, format = None):
        user = request.user
        projects = user.project_set.all()
        serializer = ProjectSerializer(projects, many = True)
        return Response(status=200, data=serializer.data)

    def post(self, request, format = None):
        serializer = ProjectSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save(user=self.request.user)
            return Response(status=status.HTTP_201_CREATED,data=serializer.data,headers={"Access-Control-Allow-Origin": "*"})
        return Response(status=status.HTTP_400_BAD_REQUEST, headers={"Access-Control-Allow-Origin": "*"})
                        
class ProjectDetail(APIView):
    
    # permission_classes = (permissions.IsAuthenticated)
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=int(pk))
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format = None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format = None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self,request, pk, format = None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# class ImageList(APIView): 
#     """
#     List images or create a new one.

#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
    
#     authentication_classes = []
#     # permission_classes = [permissions.IsAuthenticated]
#     # serializer_class = ImageSerializer
#     def get_object(self, pk):
#         try:
#             return Project.objects.get(pk=int(pk))
#         except Project.DoesNotExist:
#             raise Http404
        
#     def get(self,request,tk, *args, **kwargs):
#         target = self.get_object(pk=tk)
#         img_list = target.image_set.all()
#         image_serializer = ImageSerializer(img_list,many=True)                
#         return Response(data=image_serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, tk, *args, **kwargs):
#         image = request.FILES.get('file')
#         project = self.get_object(tk)
#         if (image):
#             (image_url,key) = upload_file_to_s3(image)
#             data = {"name": key, "url": image_url, "labels" : [], "project": int(tk)}
#             serializer = ImageSerializer(data=data)
#             if (serializer.is_valid()):
#                 serializer.save()
#                 return Response(data=serializer.data,status=status.HTTP_201_CREATED)
#             else:
#                 print(serializer.errors)
#                 return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
#     # def post(self, request,tk, format = None):
#     #     image = request.FILES.get('image')
#     #     media_storage = MediaStorage()
#     #     # media_storage.save("file_key",image)
#     #     # file_url = media_storage.url("file_key")
        
#     #     # data = {
#     #     #     'name': "Image Generated",
#     #     #     'url' : file_url 
#     #     # }
#     #     # new_image =  Image(name = "Test file", key = "some key")
#     #     # new_image.save()
#     #     # serializer = ImageSerializer(data=request.data)
        
#     #     return Response(status=200, data={"file_url": "success"})
    
# class ImageDetails(APIView):
    
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
#     permission_classes = (permissions.IsAuthenticated)
    
#     def get_object(self,pk):
#         try :
#             return Image.objects.get(pk=int(pk))
#         except Image.DoesNotExist:
#             raise Http404
        
#     def get(self, request, pk,*args,**kwargs):
#         image_seriliazer = ImageSerializer(instance=self.get_object(pk))
#         return Response(data=image_seriliazer.data,status=status.HTTP_200_OK)
     
#     def put(self, request, tk, pk, *args, **kwargs):
#         image = self.get_object(pk)
#         data = request.data
#         data["project"] = int(tk)
#         serializer = ImageSerializer(image,data=data)
#         print(serializer.is_valid())
#         if (serializer.is_valid()):
#             serializer.save()
#             return Response(data=serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#     def delete(self, request, pk,*args, **kwargs):
#         image = self.get_object(pk)
#         image.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
    
#     serializer_class = UserSerializer
#     permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    
    
# class UserDetail(generics.RetrieveAPIView):

#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    

