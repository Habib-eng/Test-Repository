from rest_framework import permissions
from urllib.parse import unquote
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
import os
import mimetypes
from django.http import FileResponse
from django.conf import settings

class MediaView(APIView):
    def get(self, request, path, format=None):
        if not os.path.exists(f"{settings.MEDIA_ROOT}/{path}"):
            return Response("No such file exists.", status=404)

        # key = request.COOKIES.get("auth", "")
        # I'm using django-rest-framework token authentication
        # token = Token.objects.filter(key=key).first()
        token = True
        if token:
            # Guess the MIME type of a file. Like pdf/docx/xlsx/png/jpeg
            mimetype, encoding = mimetypes.guess_type(path, strict=True)
            if not mimetype:
                mimetype = "text/html"
            # By default, percent-encoded sequences are decoded with UTF-8, and invalid
            # sequences are replaced by a placeholder character.
            # Example: unquote('abc%20def') -> 'abc def'.
            print(path)
            file_path = unquote(os.path.join(settings.MEDIA_ROOT, path)).encode("utf-8")
            print(file_path)
            # FileResponse - A streaming HTTP response class optimized for files.
            return FileResponse(open(file_path, "rb"), content_type=mimetype)
        return Response("Access to this file is permitted.", status=404)

class HealthView(APIView, ListModelMixin):
    def get(self, request, path, format = None):
        return Response("Django service running succefully ", status=200)