from django.db import models
from django.contrib.auth.models import User

class Auction(models.Model):
    
    AUCTION_STATUS = (
        ('open','open'),
        ('waiting','waiting'),
        ('closed','closed'),
        ('ended','ended'),
    )

    name           = models.CharField(max_length=100)
    description    = models.TextField()
    is_active      = models.BooleanField(default=True)
    auction_status = models.CharField(max_length=30,choices=AUCTION_STATUS,default='waiting')

    start_price   = models.DecimalField(max_digits=6,decimal_places=2)
    current_price = models.DecimalField(max_digits=6,decimal_places=2, default=0)

    start_date = models.DateTimeField()
    end_date   = models.DateTimeField()

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')

    def __str__(self) :
        return self.name

    def check_auction_status(self) :
        if self.auction_status == "wating" or self.auction_status == "closed" :
            raise ValueError("auction closed or not open yet...")