from .models import Auction
from rest_framework import serializers


class auction_serializer(serializers.ModelSerializer) :
    class Meta :
        model  = Auction
        fields = ['id','name','description','start_price','current_price','created_by','auction_status','is_active'] 
        read_only_fields = ['created_by']