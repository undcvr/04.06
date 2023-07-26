from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Book, BorrowedBook


# Lesson-2


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100, required=False)
    is_available = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.author = validated_data.get("author", instance.author)
        instance.is_available = validated_data.get(
            "is_available", instance.is_available
        )
        instance.save()
        return instance


class BoockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BoockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


# Lesson-2 end


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = "__all__"


class BorrowedBookGenericSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field="title", read_only=True)
    # borrower = serializers.SlugRelatedField(
    #     slug_field="username", read_only=True, many=True
    # )

    class Meta:
        model = BorrowedBook
        fields = ("id", "book", "borrower", "date_borrowed", "date_returned")
