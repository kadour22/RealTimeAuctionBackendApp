from django.urls import path
from . import views

urlpatterns = [
    path("create-auction/", views.create_auction_view.as_view()),
    path("product-service/", views.product_view_services.as_view()),
    path("product/<int:product_id>/", views.get_or_delete_product.as_view()),
    path("place-bid/<int:auction_id>/", views.palce_bid.as_view()),
]