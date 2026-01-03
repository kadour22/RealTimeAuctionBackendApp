from django.urls import path
from . import views


urlpatterns = [
    path("auctions/", views.create_auction_view.as_view()),
    path("auctions/<int:auction_id>/", views.auction_detail_view.as_view()),
    path("create_product/", views.create_product.as_view()),
    path("product/<int:product_id>/", views.get_or_delete_product.as_view()),
    path("place-bid/<int:auction_id>/", views.palce_bid.as_view()),
]

