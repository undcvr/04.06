from rest_framework import status
from rest_framework import viewsets


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book, BorrowedBook

from library_app.serializers import (
    BookSerializer,
    BoockListSerializer,
    BoockDetailSerializer,
    BorrowedBookSerializer,
    BorrowedBookGenericSerializer,
)

from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Genre
from .serializers import BookSerializer

# Реализация представления на APIView с использованием
# сеарилизатора Serializer




class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = BookSerializer

class GenreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = BookSerializer


from rest_framework.decorators import action
from rest_framework.response import Response

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['get'])
    def films(self, request, pk=None):
        genre = self.get_object()
        films = genre.film_set.all()
        serializer = BookSerializer(films, many=True)
        return Response(serializer.data)


class BooksAPIview(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(instance=book, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# Реализация представления, которое может просмотривать и добавлять записи
class BookListApiView(generics.ListCreateAPIView):
    """Просмотр списка всех книг"""

    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    serializer_class = BoockListSerializer


class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр, обновление и удаление отдельных книг
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Book.objects.all()
    serializer_class = BoockDetailSerializer


class BorrowedBookListAPIView(generics.ListCreateAPIView):
    """
    Просмотр списка всех взятых книг и создание новых
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BorrowedBookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр, обновление и удаление взятых книг
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookGenericSerializer


class BorrowedBooksReaodOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookGenericSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    # Добавить дополнительные возможности и пути.
    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[JWTAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def make_available(self, request, pk=None):
        """
        Устанавливает книгу доступной для оформления заказа.

        Args:
            request (Запрос): Объект запроса.
            pk (int): Первичный ключ книги, которую нужно сделать доступной.

        Возвращает:
            Ответ (Response): Объект ответа со статусом 204 (No Content).
        """
        book = self.get_object()
        book.is_available = True
        book.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[JWTAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def make_unavailable(self, request, pk=None):
        """
        Устанавливает книгу недоступной для оформления заказа.

        Args:
            request (Запрос): Объект запроса.
            pk (int): Первичный ключ книги, которую нужно сделать доступной.

        Возвращает:
            Ответ (Response): Объект ответа со статусом 204 (No Content).
        """
        book = self.get_object()
        book.is_available = False
        book.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BorrowedBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookGenericSerializer
    permission_classes = [IsAuthenticated]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Метод Post, который создает токен для пользователя и возвращает его в ответе.

        Аргументы:
            request: Объект HTTP-запроса.
            *args: Список аргументов переменной длины.
            **kwargs: Произвольные аргументы с ключевыми словами.

        Возвращает:
            Объект Response, содержащий словарь с ключом 'token' и его значением.
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
