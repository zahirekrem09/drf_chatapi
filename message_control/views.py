from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import GenericFileUpload, GenericFileUploadSerializer
from rest_framework.response import Response




class GenericFileUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serializer_class = GenericFileUploadSerializer
