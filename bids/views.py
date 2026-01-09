from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics

from .validations.amount_validation import validate_amount
from .serializers import bidding_serializer
from .models import Bidding
from auctions.models import Auction

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class GetBidsView(generics.ListAPIView):
    serializer_class = bidding_serializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        return Bidding.objects.filter(auction_id=auction_id).order_by('-created_at')


class PlaceBidView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, auction_id):
        auction = get_object_or_404(Auction, id=auction_id)
        auction.check_auction_status()
        amount = request.data.get('amount')
        validate_amount(amount=amount)
        bid_data = {
            'auction': auction_id,
            'amount': amount
        }
        serializer = bidding_serializer(data=bid_data)
        if serializer.is_valid():
            amount_val = float(serializer.validated_data['amount'])            
            if amount_val <= float(auction.current_price):
                return Response(
                    {"error": "the amount is less than the current price"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            bid = serializer.save(user=request.user)
            auction.current_price = amount_val
            auction.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"auction_{auction_id}",
                {
                    "type": "place_new_bid",
                    "auction_id": auction_id,
                    "amount": str(amount_val),
                    "user": request.user.id
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
