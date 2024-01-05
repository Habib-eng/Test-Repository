from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, generics
from django.conf import settings
from apps.core.services.image_service import ImageService
from apps.core.serializers import ImageMetadataSerializer
from django.http import Http404

class ImageMetadataList(APIView):

    permissions_classes = (permissions.IsAuthenticated,)
    
    # def get_dataset_object(self,dataset_id) -> Dataset:
    #     try:
    #         dataset = Dataset.objects.get(pk=dataset_id)
    #         return dataset
    #     except Dataset.DoesNotExist:
    #         raise Http404
        
    def get(self, request, project_id, format = None):
        image_service = ImageService(project_ref=project_id)
        documents = image_service.get_project_documents()
        serializer = ImageMetadataSerializer(documents, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    ### within this request we get a multipart/formdata contain image: file, dataset_ref: uuid
    def post(self, request, project_id, format = None):
        files = request.FILES.getlist("file")
        image_service = ImageService(project_ref=project_id)
        document = image_service.store_document(files)
        serializer = ImageMetadataSerializer(document)
        return Response(status=status.HTTP_201_CREATED,data=serializer.data)
    
class ImageMetadataDetail(APIView):
    
    permissions_classes = (permissions.IsAuthenticated,)

    def put(self, request, project_id, document_id, format = None):
        image_service = ImageService()
        document = image_service.update_document_annotations(document_id, request.data)    
        serializer = ImageMetadataSerializer(document)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
