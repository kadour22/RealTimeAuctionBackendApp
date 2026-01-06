from rest_framework import generics
from .serializers import auction_serializer
from .models import Auction

class list_create_auction(generics.ListCreateAPIView) :
    serializer_class = auction_serializer
    queryset = Auction.objects.select_related('created_by').all()

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
    

class retrieve_update_delete_auction(generics.RetrieveUpdateDestroyAPIView) :
    serializer_class = auction_serializer
    queryset = Auction.objects.select_related('created_by').all()
    lookup_field = 'id'
    