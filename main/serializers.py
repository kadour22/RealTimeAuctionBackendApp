from rest_framework import serializers
from .models import *

class auction_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Auction
        fields= "__all__"

class bid_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Bid
        fields= "__all__"