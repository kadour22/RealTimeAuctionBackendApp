from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import auction_serializer
from .models import Auction
from .validations.check_auction_status import check_auction_status

class list_create_auction(APIView) :
    def get(self, request) :
        
        open_auctions    = Auction.objects.select_related("created_by").filter(auction_status="open").all()
        waiting_auctions = Auction.objects.select_related("created_by").filter(auction_status="waiting").all()
        ended_auctions   = Auction.objects.select_related("created_by").filter(auction_status="ended").all()

        auctions_data = {
            "open" : auction_serializer(open_auctions,many=True).data , 
            "waiting":auction_serializer(waiting_auctions,many=True).data,
            "ended":auction_serializer(ended_auctions,many=True).data
        }
        
        return Response(auctions_data, status = 200)
    
    def post(self, request) :
        serializer = auction_serializer(data=request.data)
        if serializer.is_valid() :
            serializer.save(created_by=request.user)
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

class retrieve_update_delete_auction(generics.RetrieveUpdateDestroyAPIView) :
    serializer_class = auction_serializer
    queryset = Auction.objects.select_related('created_by').all()
    lookup_field = 'id'
    