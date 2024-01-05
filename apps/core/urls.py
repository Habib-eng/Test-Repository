from django.urls import path
from apps.core.views.project_views import  ProjectList, ProjectDetail
from apps.core.views.prebuilt_ocr_model_views import PrebuiltOCRModelDetail, PrebuiltOCRModelList
from apps.core.views.subscription_views import SubscriptionList, AttemptList
from apps.core.views.project_views import DocumentList
from apps.core.views.image_views import ImageMetadataList, ImageMetadataDetail

urlpatterns = [
    path('document/', DocumentList.as_view()),
    path('prebuilt-ocr/', PrebuiltOCRModelList.as_view()),
    path('prebuilt-ocr/<int:pk>/', PrebuiltOCRModelDetail.as_view()),
    path('project/', ProjectList.as_view()),
    path('project/<int:pk>/', ProjectDetail.as_view()),
    path('project/<str:project_id>/document/', ImageMetadataList.as_view()),
    path('project/<str:project_id>/document/<str:document_id>/', ImageMetadataDetail.as_view()),
    path('subscription/', SubscriptionList.as_view()),
    path('subscription/<int:subscription_id>/attempt', AttemptList.as_view()),
    # path('dataset/<int:pk>/', DatasetDetail.as_view()),
]
