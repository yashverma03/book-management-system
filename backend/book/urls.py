from django.urls import path
from book.views import books, book_detail, google_books

app_name = 'book'

urlpatterns = [
    path('', books, name='books'),  # GET /api/v1/books, POST /api/v1/books
    path('/<int:book_id>', book_detail, name='book_detail'),  # GET, PATCH, DELETE /api/v1/books/<id>
    path('/google', google_books, name='google_books'),  # GET /api/v1/books/google
]
