from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Project, DocumentType, Attempt, DocumentMetadata, Subscription, Plan, CustomUser, PrebuiltOCRModel])