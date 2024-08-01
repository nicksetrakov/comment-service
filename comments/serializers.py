import io
import sys

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import magic
from user.serializers import UserSerializer
from .models import User, Comment
from django.core.files.images import get_image_dimensions


class CommentSerializer(serializers.ModelSerializer):
    username = SlugRelatedField(
        slug_field="username", read_only=True, source="user"
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "username",
            "email",
            "homepage",
            "text",
            "parent",
            "created_at",

        ]
        read_only_fields = ["id", "created_at", "username"]


class CommentListSerializer(CommentSerializer):

    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "username",
            "email",
            "homepage",
            "text",
            "parent",
            "created_at",
            "attachment",
            "replies",
        ]
        read_only_fields = ["id", "created_at", "username"]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class CommentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "attachment"]

    def validate_attachment(self, value):

        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_buffer(value.read())
        value.seek(0)  # Вернем указатель файла в начало

        # Допустимые форматы изображений и текстов
        valid_image_mime_types = ["image/jpeg", "image/png", "image/gif"]
        valid_text_mime_types = ["text/plain"]

        if file_mime_type in valid_image_mime_types:
            # Проверка размеров изображения
            image = Image.open(value)
            width, height = image.size

            if width > 320 or height > 240:
                # Пропорциональное уменьшение изображения до заданных размеров
                image.thumbnail((320, 240))
                output = io.BytesIO()
                image.save(output, format=image.format)
                output.seek(0)  # Вернем указатель файла в начало
                value = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    value.name,
                    file_mime_type,
                    sys.getsizeof(output),
                    None
                )

        elif file_mime_type in valid_text_mime_types:
            # Проверка размера текстового файла
            if value.size > 1024 * 100:
                raise serializers.ValidationError("File size cannot exceed 100 KB for text files.")

        else:
            raise serializers.ValidationError("Unsupported file type.")

        return value
