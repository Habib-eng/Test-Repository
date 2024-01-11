from apps.core.repositories.image_repository import ImageRepository
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from mimetypes import guess_type
from uuid import uuid4
import os
from PIL import Image

class ImageService:
    
    def __init__(self, project_ref = None) -> None:
        self.repository = ImageRepository()
        self.project_ref = project_ref
    
    def store_document(self, files: MultiValueDict) -> str:
        for file in files:
            metadata = self.get_document_metadata(file)
            url = self.save_document(file)
            image = self.repository.create_image(name=metadata["name"], extension=metadata["extension"], width=metadata['width'], height=metadata['height'],url=url,project_ref=self.project_ref)
            return image
    
    def save_document(self, uploaded_file: InMemoryUploadedFile) -> str:
        generated_filename = str(uuid4()).replace("-","") + uploaded_file.name
        filepath = os.path.join(settings.DOCUMENT_ROOT,generated_filename)
        with open(filepath,"wb") as f:
            f.write(uploaded_file.open("rb").read())
        url = settings.APP_URL + settings.DOCUMENT_URL + generated_filename
        return url
    
    def get_document_metadata(self, uploaded_file: InMemoryUploadedFile) -> dict:
        image = Image.open(uploaded_file)
        metadata = {
            "name" : uploaded_file.name,
            "width" : image.width,
            "height" : image.height,
            "extension" : guess_type(uploaded_file.name)[0]
        }
        print(image)
        return metadata
    
    def get_project_documents(self):
        data = self.repository.list_images(project_ref=self.project_ref)
        return data
    
    def update_document_annotations(self, id, annotations):
        document = self.repository.update_document(id, annotations=annotations)
        return document
    
