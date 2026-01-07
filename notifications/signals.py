from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.db.models.signals import post_save
from django.dispatch import receiver

from auctions.models import Auction
from .models import Notification

@receiver(post_save, sender=Auction)
def send_notification(sender, instance, created, **kwargs) :
    if created :
        notify = Notification.objects.create(
            message = f"{instance.created_by.username} created an auction with name : {instance.name}"
        )
        print(notify)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type":"new_notification",
                "message":notify.message,
                "is_read":notify.is_read,
                "created_at":notify.created_at.isoformat()
            }
        )