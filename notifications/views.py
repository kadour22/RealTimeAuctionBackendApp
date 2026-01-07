from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Notification
from .serializers import notification_serializer

class notifications_list(APIView) :
    def get(self, request) :
        notifications = Notification.objects.all()
        serializer    = notification_serializer(notifications, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

class notification_detail_view(APIView) :
    def get(self, request,notification_id) :
        notification = get_object_or_404(Notification,id=notification_id)
        channel_layer = get_channel_layer()
        serializer = notification_serializer(notification,many=False)
        async_to_sync(channel_layer.group_send)(
            "notification_read",
            {
                "type":"notification_read",
                "notification_id":notification.id
            }
        )
        return Response(serializer.data,status=200)

