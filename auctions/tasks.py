from celery import shared_task
from .models import Auction
from django.utils import timezone

@shared_task
def check_auction_timing():
    today = timezone.now().date()
    auctions = Auction.objects.all()
    for auction in auctions:
        if auction.start_date and auction.end_date:
            if today < auction.start_date:
                auction.auction_status = "waiting"
            elif auction.start_date <= today <= auction.end_date:
                auction.auction_status = "open"
                print(f"Auction {auction.id} is open")
            elif today > auction.end_date:
                auction.auction_status = "closed"
                auction.is_active = False
                print(f"Auction {auction.id} is closed")
            auction.save() 

    print("hello from celery")