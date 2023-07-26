from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CustomAuthToken,
    BooksAPIview,
    BookViewSet,
    BookListApiView,
    BookDetailAPIView,
    BorrowedBookViewSet,
    BorrowedBooksReaodOnlyViewSet,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
router.register(r"borrowed-books", BorrowedBookViewSet, basename="borrowedbook")
router.register(r"borrowed-book-list", BorrowedBooksReaodOnlyViewSet, basename="borrowed_book_list")


urlpatterns = [
    # Пути views сериализатор которых не использует ModelSerializer - begin
    path("bookslist/", BooksAPIview.as_view(), name="bookslist"),
    path("bookslist/<int:pk>/", BooksAPIview.as_view(), name="book_change"),
    # Пути views сериализатор которых не использует ModelSerializer - end
    path("books_list/", BookListApiView.as_view(), name="books_list"),
    path("book_detail/<int:pk>/", BookDetailAPIView.as_view(), name="book_detail"),
    # JWT проверка - begin
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # JWT проверка - end
    path("api-token-auth/", CustomAuthToken.as_view()),
] + router.urls
