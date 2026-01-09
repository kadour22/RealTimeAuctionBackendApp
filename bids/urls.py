from django.urls import path
from . import views

urlpatterns = [
    path('get-bids/<int:auction_id>/', views.GetBidsView.as_view()),
    path('place-bid/<int:auction_id>/', views.PlaceBidView.as_view()),
]
