from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import GenericFileUploadSerializer
from .models import GenericFileUpload
from rest_framework.response import Response


class GenericFileUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serializer_class = GenericFileUploadSerializer
