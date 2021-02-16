from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import GenericFileUploadSerializer, MessageSerializer
from .models import GenericFileUpload, Message, MessageAttachment
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class GenericFileUploadView(ModelViewSet):
    queryset = GenericFileUpload.objects.all()
    serializer_class = GenericFileUploadSerializer


class MessageView(ModelViewSet):
    queryset = Message.objects.select_related(
        "sender", "receiver").prefetch_related("message_attachments")
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except:
            pass
        attachments = request.data.pop("attachments", None)

        if str(request.user.id) != str(request.data.get("sender_id", None)):
            raise Exception("only sender can create a message")

        attachments = request.data.pop('attachments', None)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if attachments:
            MessageAttachment.objects.bulk_create([MessageAttachment(
                **attachment, message_id=serializer.data["id"]) for attachment in attachments])
            message_data = self.get_queryset().get(id=serializer.data["id"])
            return Response(self.serializer_class(message_data).data, status=201)

        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        attachments = request.data.pop("attachments", None)
        instance = self.get_object()

        serializer = self.serializer_class(
            data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        MessageAttachment.objects.filter(message_id=instance.id).delete()

        if attachments:
            MessageAttachment.objects.bulk_create([MessageAttachment(
                **attachment, message_id=instance.id) for attachment in attachments])

            message_data = self.get_object()
            return Response(self.serializer_class(message_data).data, status=200)

        return Response(serializer.data, status=200)
