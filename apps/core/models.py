import uuid
from djongo import models as nosql_models
from django.db import models
from apps.core.enums import ProjectState, ImageExtension
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from apps.core.managers import CustomUserManager, ImageMetadataManager

class PrebuiltOCRModel(models.Model):
    name = models.CharField(max_length=255)
    document = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = models.URLField(null=False,default="")
    category = models.CharField(max_length=5,null=False,default="")
    ocr_endpoint = models.URLField(default=None,null=True)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(default=None, max_length=30,null=True)
    lastname = models.CharField(default=None, max_length=30,null=True)
    company = models.CharField(default=None, max_length=30,null=True)
    position = models.CharField(default=None, max_length=30,null=True)
    phoneNumber = models.CharField(default=None, max_length=30,null=True)
    email = models.EmailField(unique=True, null=False)
    country = models.CharField(default=None, max_length=30,null=True)
    is_staff = models.BooleanField(default=False,null=True)
    is_active = models.BooleanField(default=True,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(PrebuiltOCRModel,through="subscription",related_name="products")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Plan(models.Model):
    name = models.CharField(max_length=255)
    price_per_year = models.CharField(max_length=255)
    usage_limit = models.IntegerField(default=None,null=True)    
    description = models.TextField()
    features = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField()

class Subscription(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(PrebuiltOCRModel, on_delete=models.DO_NOTHING)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    usage_rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product','owner','plan')

class DocumentMetadata(models.Model):
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=255,choices=[(ext.value,None) for ext in list(ImageExtension)])
    uploaded_date = models.DateTimeField(auto_now_add=True)

class Attempt(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING)
    document_location = models.URLField(default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True )
    result = models.JSONField(default=None,null=True)
    document_metadata = models.OneToOneField(DocumentMetadata,on_delete=models.DO_NOTHING,primary_key=True)

class DocumentType(models.Model):
    name = models.CharField(max_length=255, default=None, null=False)
    image_url = models.URLField()
    comment = models.CharField(max_length=255, default=None, null=True)

class Project(models.Model):
    
    class ProjectType(models.IntegerChoices):
        BASED_ON_PREBUILT_MODEL = 0
        CUSTOM_MODEL = 1

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    based_document = models.ForeignKey(DocumentType, on_delete=models.PROTECT,null=True)
    code = models.CharField(max_length=255, null=False, unique=True)
    type = models.IntegerField(choices=ProjectType.choices)
    state = models.CharField(max_length=20,choices=ProjectState.choices, default=ProjectState.CREATED)
    description = models.TextField(null=True)
    labels = models.JSONField(default=None,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.code

class ImageMetadata(nosql_models.Model):
    _id = nosql_models.ObjectIdField()
    name = nosql_models.CharField(max_length=255)
    extension = nosql_models.CharField(max_length=255,choices=[(ext.value,None) for ext in list(ImageExtension)])
    width = nosql_models.IntegerField()
    height = nosql_models.IntegerField()
    url = nosql_models.URLField(max_length=255,default="")
    uploaded_date = nosql_models.DateTimeField(auto_now_add=True)
    annotations = nosql_models.TextField()
    project_ref = nosql_models.CharField(max_length=255)
    objects = ImageMetadataManager()