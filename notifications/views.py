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
    