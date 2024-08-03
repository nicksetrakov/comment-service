from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .tasks import send_reply_notification


@receiver(post_save, sender=Comment)
def handle_comment_reply(sender, instance, created, **kwargs):
    if created and instance.parent:
        send_reply_notification.delay(
            instance.parent.email, instance.parent.text, instance.text
        )
