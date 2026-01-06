from django.db import models
from auctions.models import Auction
from django.contrib.auth.models import User

class Bidding(models.Model) :
    
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    auction    = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auctions')
    amount     = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} => {self.auction.name}"
    