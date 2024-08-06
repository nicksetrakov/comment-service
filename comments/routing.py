from django.urls import re_path

from comments.consumers import CommentConsumer

websocket_urlpatterns = [
    re_path(r"ws/comments/(?P<comment_id>\d+)/$", CommentConsumer.as_asgi()),
]
