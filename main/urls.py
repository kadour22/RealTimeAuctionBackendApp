from django.urls import path
from . import views

urlpatterns = [
    path("place-bid/<int:auction_id>/", views.palce_bid.as_view()),
]