from django.urls import path
from . import views

urlpatterns = [
    path("notification_list/" , views.notifications_list.as_view()),
    path("notification/<int:notification_id>/" , views.notification_detail_view.as_view()),
]