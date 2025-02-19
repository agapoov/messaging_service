from django.utils import timezone
from rest_framework import generics, viewsets

from .models import Client, Mailing
from .serializers import ClientSerializer, MailingSerializer
from .tasks import sending_processing


class MailingCreateView(generics.CreateAPIView):
    serializer_class = MailingSerializer

    def perform_create(self, serializer):
        mailing = serializer.save()
        if mailing.start_time <= timezone.now():
            sending_processing.delay(mailing.id)
        else:
            sending_processing.apply_async(
                args=[mailing.id],
                eta=mailing.start_time
            )


class MailingListView(generics.ListAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingDetailView(generics.RetrieveAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
