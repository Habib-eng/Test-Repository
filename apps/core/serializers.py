from apps.core.models import Project, PrebuiltOCRModel, DocumentMetadata,  ImageMetadata, CustomUser, Plan, Subscription, Attempt, DocumentType
from rest_framework.serializers import ModelSerializer, CharField, IntegerField
from apps.core.enums import ProjectState
from djongo.models.fields import ObjectIdField


class PrebuiltOCRModelSerializer(ModelSerializer):
    """
     A class used to serialize a prebuilt model
    """
    class Meta:
        model = PrebuiltOCRModel
        fields = ['id', 'name', 'document','description','category','image']
class DocumentTypeSerializer(ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name','image_url', 'comment')

class ProjectSerializer(ModelSerializer):
    based_document = DocumentTypeSerializer()
    class Meta:
        model = Project
        fields = ['id', 'type', 'description', 'based_document', 'code', 'state', 'labels', 'created_on']
        read_only_fields = ['id', 'state', 'created_on']

class ImageMetadataSerializer(ModelSerializer):

    class Meta:
        model = ImageMetadata
        fields = ('_id','name', 'extension', 'width', 'height', 'url','annotations', 'uploaded_date', 'project_ref')
        read_only_field = ('_id','uploaded_date', 'width', 'height', 'url', 'name','annotations', 'extension')

class UserSerializer(ModelSerializer):
    email = CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'firstname', 'lastname', 'company', 'phoneNumber', 'country', 'position']

class ProductSerializer(ModelSerializer):
    
    class Meta:
        model = PrebuiltOCRModel
        fields = ('id','name','description','image','category')

class PlanSerializer(ModelSerializer):

    class Meta:
        model = Plan
        fields = ('id','name','description','usage_limit')


class SubscriptionSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    product_id = IntegerField(write_only=True)
    plan_id = IntegerField(write_only=True)
    
    class Meta:
        model = Subscription
        fields = ('id','product','product_id', 'plan_id', 'plan','start_time','usage_rate','end_time','is_active')
        read_only = ('id','product', 'plan','start_time','usage_rate','end_time','is_active',)

class DocumentMetadataSerializer(ModelSerializer):
    class Meta: 
        model = DocumentMetadata
        fields = ('extension','name')

class AttemptSerializer(ModelSerializer):
    document_metadata = DocumentMetadataSerializer()

    class Meta:
        model = Attempt
        fields = ('created_at','document_location','document_metadata','result')
