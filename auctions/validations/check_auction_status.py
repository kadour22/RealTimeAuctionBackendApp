from rest_framework.response import Response

def check_auction_status(auction) :
    if auction.auction_status == "waiting" or auction.auction_status == "closed" :
        return Response({"message":"the auction is not open or is closed"}) 
    return auction