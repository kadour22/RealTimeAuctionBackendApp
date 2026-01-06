from django.urls import path
from . import views

urlpatterns = [
    path('list-create-auction/', views.list_create_auction.as_view()),
    path('auction/<int:id>/', views.retrieve_update_delete_auction.as_view())
]