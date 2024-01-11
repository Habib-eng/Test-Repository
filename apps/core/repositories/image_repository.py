from apps.core.models import ImageMetadata
from apps.core.serializers import ImageMetadataSerializer
from bson.objectid import ObjectId
import json
class ImageRepository:
    def create_image(self, name: str, extension: str, width: int, height: int, url: str, project_ref: str, annotations="[]") -> str:
        print("Creating new image ...")
        image = None
        try:
            image = ImageMetadata(name= name, extension= extension, width = width, height = height, url= url, project_ref = project_ref, annotations="[]")
            image.save(using="nosql_database")
        except Exception as e:
            print(e)
            print("Error creation model ")
        return image
    
    def list_images(self, project_ref):
        images = ImageMetadata.objects.using("nosql_database").filter(project_ref=project_ref)
        return images
    
    def update_document(self, doc_id, annotations):
        target = None
        try:
            target = ImageMetadata.objects.filter(_id=ObjectId(doc_id)).first()
            target.annotations = json.dumps(annotations)
            target.save()
        except Exception as e:
            print(e)
        return target