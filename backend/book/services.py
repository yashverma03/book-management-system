from django.utils import timezone as django_timezone
from book.models import Book
from book.serializers import BookSerializer
from utils.exceptions import NotFoundException, ConflictException


class BookService:
  def create_book(self, dto, userId) -> dict:
    """
    Create a new book

    Args:
        dto: Dictionary with book data (title, author, description, price, isbn)
        userId: User ID who is adding the book

    Returns:
        dict: Serialized book data

    Raises:
        ConflictException: If ISBN already exists
    """
    # Check if ISBN already exists (if provided)
    if dto.get('isbn'):
      existing_book = Book.objects.filter(isbn=dto['isbn'], deleted_at=None).first()
      if existing_book:
        raise ConflictException('Book with this ISBN already exists')

    # Set added_by to the user ID
    dto['added_by_id'] = userId

    book = Book.objects.create(**dto)
    book_data = BookSerializer(book).data
    return book_data

  def get_books(self, filters=None) -> list:
    """
    Get all books with optional filters.
    Includes user data via left join.

    Args:
        filters: Dictionary with optional filters:
            - title: Filter by title (case-insensitive partial match)
            - isbn: Filter by exact ISBN
            - author: Filter by author (case-insensitive partial match)
            - added_by_user: Filter by user ID who added the book

    Returns:
        list: List of serialized book data with nested user data
    """
    queryset = Book.objects.filter(deleted_at=None).select_related('added_by')

    if filters:
      # Filter by title (case-insensitive partial match)
      if filters.get('title'):
        queryset = queryset.filter(title__icontains=filters['title'])

      # Filter by ISBN (exact match)
      if filters.get('isbn'):
        queryset = queryset.filter(isbn=filters['isbn'])

      # Filter by author (case-insensitive partial match)
      if filters.get('author'):
        queryset = queryset.filter(author__icontains=filters['author'])

      # Filter by added_by_user (user ID)
      if filters.get('added_by_user'):
        queryset = queryset.filter(added_by_id=filters['added_by_user'])

    books = queryset.order_by('-created_at')
    return [BookSerializer(book).data for book in books]

  def get_book_by_id(self, book_id) -> dict:
    """
    Get a book by ID.
    Includes user data via left join.

    Args:
        book_id: Book ID

    Returns:
        dict: Serialized book data with nested user data

    Raises:
        NotFoundException: If book not found or deleted
    """
    try:
      book = Book.objects.select_related('added_by').get(id=book_id, deleted_at=None)
      book_data = BookSerializer(book).data
      return book_data
    except Book.DoesNotExist:
      raise NotFoundException('Book not found')

  def update_book(self, book_id, dto) -> dict:
    """
    Update a book by ID

    Args:
        book_id: Book ID
        dto: Dictionary with fields to update

    Returns:
        dict: Serialized updated book data

    Raises:
        NotFoundException: If book not found or deleted
        ConflictException: If ISBN already exists (when updating ISBN)
    """
    try:
      book = Book.objects.get(id=book_id, deleted_at=None)
    except Book.DoesNotExist:
      raise NotFoundException('Book not found')

    # Check if ISBN is being updated and if it conflicts with existing book
    if 'isbn' in dto and dto['isbn'] and dto['isbn'] != book.isbn:
      existing_book = Book.objects.filter(isbn=dto['isbn'], deleted_at=None).exclude(id=book_id).first()
      if existing_book:
        raise ConflictException('Book with this ISBN already exists')

    # Update book fields
    for key, value in dto.items():
      setattr(book, key, value)

    book.save()
    book_data = BookSerializer(book).data
    return book_data

  def delete_book(self, book_id) -> None:
    """
    Soft delete a book by ID

    Args:
        book_id: Book ID

    Raises:
        NotFoundException: If book not found or already deleted
    """
    updated_count = Book.objects.filter(
      id=book_id,
      deleted_at=None
    ).update(deleted_at=django_timezone.now())

    if updated_count == 0:
      raise NotFoundException('Book not found or already deleted')
