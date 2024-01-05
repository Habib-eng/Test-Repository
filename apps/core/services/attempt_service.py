from hashlib import md5
from elasticsearch import Elasticsearch
import requests
import os
from .adapters import adapt
from ..models import DocumentMetadata, Attempt
from django.conf import settings
from pdf2image import convert_from_path

ALLOWED_EXTENSIONS = ["png", "pdf", "jpg", "jpeg"]
AUTH_HEADER = "AMI_bEcfJ8ysBT7Cu92v"
client = Elasticsearch("http://localhost:9200")
TEXT_DETECTION_API_URL = "http://54.172.239.43:8000/detect/19"

class AttemptService:
    
    def __init__(self, subscription) -> None:
        self.subscription = subscription
        self.handler = DocumentCheckerHandler(FileExistHandler(None))
                
    def create(self,file):
        res = self.handler.handle(file)

        if (file.split(".")[-1] == "pdf"):
            pdf_spliter = PdfSpliter(file)
            pages = pdf_spliter.split_pdf()
        else:
            pages = [file]

        ### Document url
        document_url = settings.APP_URL + settings.DOCUMENT_URL + file.split("/")[-1]

        ### pages variable contain a filepaths list
        ocr = Ocr(ocr_id=self.subscription.product.id, ocr_endpoint=self.subscription.product.ocr_endpoint)
        res = ocr.build_response(pages)

        ### saving document metadata
        doc_metadata = DocumentMetadata.objects.create(name=file.split("/")[-1], extension=file.split(".")[-1])
        doc_metadata.save()

        attempt = Attempt.objects.create(subscription=self.subscription, document_location=document_url, document_metadata=doc_metadata,result=res)
        attempt.save()

        self.subscription.usage_rate+=1
        self.subscription.save()
        return res

class AbstractHandler(object):
    
    def __init__(self, nxt):
        
        """change or increase the local variable using nxt"""
        self._msg = None
        self._nxt = nxt
 
    def handle(self, file):
 
        """It calls the processfile through given file"""
 
        handled = self.processfile(file)
 
        """case when it is not handled"""
 
        if handled and self._nxt:
            self._nxt.handle(file)
        else:
            return self._msg
 
    def processfile(self, file):
 
        """throws a NotImplementedError"""
 
        raise NotImplementedError('First implement it !')

class DocumentCheckerHandler(AbstractHandler):

    def processfile(self, file):
        print(f"Handler 1 : {self.__class__.__name__}")
        file_ext = file.split(".")[-1]
        if file_ext in ALLOWED_EXTENSIONS:
            return True
        else:
            self._msg = {"details": "File extension not allowed"}

class FileExistHandler(AbstractHandler):

    def processfile(self, file):
        with open(file, "rb") as f:
            raw_content = f.read()
        hash_file = md5(raw_content).hexdigest()

        # res = client.search(index="documents",query={
        #     "match": {
        #         "hash": hash_file
        #     }
        # })
        # founded = res["hits"]["total"] > 1
        # if founded:
        #     self._msg = res['hits']['hits']['_source']
        return True

class Ocr:

    def __init__(self, ocr_id, ocr_endpoint):
        self.ocr_id = ocr_id
        self.ocr_endpoint = ocr_endpoint

    def build_response(self, pages):
        res = []
        for page in pages:
            res.append({
                "url": settings.APP_URL + settings.DOCUMENT_URL + page.split("/")[-1],
                "data": self.construct_key_val_pairs(page),
                "polygones": self.construct_polygones(page),
                "tables": []
            })
        return res
    
    def construct_polygones(self, file):
        try:
            res = requests.post(TEXT_DETECTION_API_URL,files={"file": open(file,"rb")})
            polygones = res.json()['det_polygones']
        except requests.RequestException as e:
            polygones = []
        return polygones

    def construct_key_val_pairs(self, file):
        try:
            res = requests.post(self.ocr_endpoint, files={"file": open(file,"rb")}, headers={'Authorization': AUTH_HEADER})
            print(res.status_code)
            print(self.ocr_endpoint)
            print(res.json())
            if (res.status_code == 200):
                data = adapt(self.ocr_id,res.json())
            else:
                data = []  
            return data
        except requests.RequestException as e:
            return [] 
    
class PdfSpliter:

    def __init__(self,pdf_path) -> None:
        self.pdf_path = pdf_path

    def split_pdf(self):
        pages = []
        images = convert_from_path(self.pdf_path)
        for i in range(len(images)):
            page_path = os.path.join(settings.DOCUMENT_ROOT,f"page{str(i)}.jpg")
            images[i].save(page_path, 'JPEG')
            pages.append(page_path)
        return pages

