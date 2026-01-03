from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class user_serializer(serializers.ModelSerializer) :
    class Meta :
        model = User
        fields= ["id", "username"]


class bids_serializer(serializers.ModelSerializer) :
    user = user_serializer(read_only=True)
    class Meta :
        model = Bid
        fields= ["amount", "user"]

class auction_serializer(serializers.ModelSerializer) :
    bids = bids_serializer(many=True, read_only=True)
    class Meta :
        model = Auction
        fields= ["id","name", "start_price", "current_price", "start_date", "ends_date", "created_by", "product", "bids"]

class bid_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Bid
        fields= ["amount", "user", "auction"]

class products_serializer(serializers.ModelSerializer) :
    class Meta :
        model = Product
        fields = [
            "name", "price", "image", "description"
        ]