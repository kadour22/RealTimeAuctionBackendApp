from rest_framework import serializers
from .models import Notification

class notification_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Notification
        fields = ["message","is_read","created_at"]