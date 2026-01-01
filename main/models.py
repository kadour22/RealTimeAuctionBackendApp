from django.db import models
from django.contrib.auth.models import User


class Product(models.Model) :
    name  = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    image = models.ImageField(upload_to='products')
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

class Auction(models.Model) :
    name = models.CharField(max_length=100)
    start_price = models.DecimalField(max_digits=6,decimal_places=2)
    current_price = models.DecimalField(max_digits=6,decimal_places=2, null=True)
    start_date  = models.DateField()
    ends_date   = models.DateField()
    created_by  = models.ForeignKey(User , on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='auction', null=True)

    def __str__(self) :
        return f"{self.name} , {self.product.name}"

    def __str__(self) :
        return self.name

class Bid(models.Model) :
    user    = models.ForeignKey(User , on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE,related_name='bids')
    amount  = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return f"the user : {self.user.username} create a bid for {self.auction.name} with amount : {self.amount} $"