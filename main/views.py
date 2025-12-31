from rest_framework.generics import GenericAPIView 
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status 

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *


class palce_bid(GenericAPIView , CreateModelMixin) :
    serializer_class = bid_serializer

    def post(self, request, auction_id) :
       
        auction = get_object_or_404(Auction , id=auction_id)
        serializer = serializers.get_serializer(data=request.data)
        if serializer.is_valid() :
            
            amount = serializers.validated_data["amount"]     
            if amount <= auction.current_price :
                return Response({
                    "error" : "amount should be great than current place"
                })
            
            bid = Bid.objects.create(
                auction=auction,
                amount=amount,
                user = request.User
            )

            auction.current_price = amount
            auction.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"auction_{auction.id}",{
                    "type":"new_bid",
                    "auction_id":auction.id ,
                    "user":request.user
                }
            )
            return Response("bid created.." , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_404_NOT_FOUND)