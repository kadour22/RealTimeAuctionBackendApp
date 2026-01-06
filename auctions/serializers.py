from .models import Auction
from rest_framework import serializers


class auction_serializer(serializers.ModelSerializer) :
    class Meta :
        model  = Auction
        fields = "__all__"
        read_only_fields = ['created_by']