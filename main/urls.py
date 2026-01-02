from django.urls import path
from . import views

urlpatterns = [
    path("create-auction/", views.create_auction_view.as_view()),
    path("place-bid/<int:auction_id>/", views.palce_bid.as_view()),
]