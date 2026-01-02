from .models import *
from .serializers import *
from .services.products_services import (
    create_product, delete_product, get_product_by_id
)
from rest_framework.generics import GenericAPIView 
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404



class create_auction_view(APIView) :
    def post(self, request) :
        serializer = auction_serializer(data = request.data)
        if serializer.is_valid() :

            start_date = serializer.validated_data["start_date"]
            ends_date  = serializer.validated_data["ends_date"]

            if ends_date >= start_date :
                return Response({"error":"ends date should be great than start date"})
            
            serializer.save(created_by=request.user)
            return Response(serializer.data , status=201)
        
        return Response(serializer.errors , status=400)


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