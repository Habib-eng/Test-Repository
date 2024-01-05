from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum

class ProjectState(models.TextChoices):
    CREATED = "Created", _("Created")
    IMAGES_IMPORTED = "Images imported", _("Images imported")
    IMAGES_LABLED = "Images labeled", _("Images labeled")
    MODEL_TRAINED = "Model Trained", _("Model Trained")
    MODEL_DEPLOYED = "Model Deployed", _("Model Deployed")

class ImageExtension(Enum):
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"