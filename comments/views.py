from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Comment
from .permissions import IsOwnerOrAdmin
from .serializers import CommentSerializer, CommentListSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of comments",
        description="Retrieve a list of all top-level comments. Accessible by authenticated users.",
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Ordering of the comments (e.g., ?ordering=user__username or ?ordering=-created_at).",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={200: CommentListSerializer(many=True)},
        examples=[
            OpenApiExample(
                "Comment list example",
                value=[
                    {
                        "id": 1,
                        "username": "user1",
                        "email": "user1@example.com",
                        "homepage": "http://example.com",
                        "text": "This is a comment.",
                        "parent": None,
                        "created_at": "2024-06-18T12:00:00Z",
                        "attachment": "http://example.com/uploads/attachments/user1-uuid.jpg",
                        "replies": [],
                    }
                ],
            )
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve a single comment",
        description="Retrieve the details of a specific comment by its ID. Accessible by authenticated users.",
        responses={200: CommentListSerializer},
    ),
    create=extend_schema(
        summary="Create a new comment",
        description="Create a new comment. Accessible by authenticated users.",
        responses={201: CommentSerializer},
    ),
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdmin,
    ]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["user__username", "email", "created_at"]

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = Comment.objects.filter(parent=None)

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CommentListSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.replies.all().delete()
        instance.delete()

    @action(detail=True, methods=["post"])
    def reply(self, request, pk=None):
        parent_comment = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, parent=parent_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
