from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_reply_notification(email, comment_text, reply_text):
    send_mail(
        "New reply for your comment",
        f"Your comment: {comment_text}\n\nReply: {reply_text}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
