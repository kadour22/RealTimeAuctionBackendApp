from .models import *
from .serializers import *
from rest_framework.generics import GenericAPIView 
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404

class create_product(GenericAPIView , CreateModelMixin):
    serializer_class = products_serializer
    def post(self, request) :
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class get_or_delete_product(APIView) :
    def delete(self,request,product_id):
        product = get_object_or_404(id=product_id)
        product.delete()
        return Response({"message":"product deleted"},status=200)
    def get(self,request,product_id):
        product = get_object_or_404(id=product_id)
        serializer = products_serializer(product,many=False)
        return Response(serializer.data, status=200)



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