from rest_framework import permissions
from rest_framework import mixins
from rest_framework import generics
from apps.core.models import PrebuiltOCRModel
from apps.core.serializers import PrebuiltOCRModelSerializer

class PrebuiltOCRModelList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    """
    A class used to create new prebuilt model or list all created prebuilt models

    Attributes
    ----------

    Methods
    -------
        get(request, *args, **kwargs)
            retrieve the list of prebuiltOCR models
        post(request, *args, **kwargs)
            create new prebuilt ocr models
    """

    # permission_classes = (permissions.IsAuthenticated,)
    queryset = PrebuiltOCRModel.objects.all()
    serializer_class = PrebuiltOCRModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class PrebuiltOCRModelDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    
    """
    A class used to retrieve, modify or delete a prebuilt model based on its id passed within the request

    Attributes
    ----------

    Methods
    -------
        get(request, *args, **kwargs)
            retreive an prebuilt OCR model by its id
        put(request, *args, **kwargs)
            modify an existant prebuilt OCR models
        delete(request, *args, **kwargs)
            delete an existant prebuilt OCR model by its id
    """

    permission_classes = (permissions.IsAuthenticated,)
    queryset = PrebuiltOCRModel.objects.all()
    serializer_class = PrebuiltOCRModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)