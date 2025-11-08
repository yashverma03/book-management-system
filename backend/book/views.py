from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from book.dto.create_book_dto import CreateBookDto
from book.dto.update_book_dto import UpdateBookDto
from book.dto.get_books_dto import GetBooksDto
from book.services import BookService
from utils.dto_validator import DTOValidator
from decorators.roles import roles
from user.models import UserRole

book_service = BookService()

def get_books(request):
  filters = DTOValidator.validate(GetBooksDto, request.query_params)
  result = book_service.get_books(filters)
  return Response(result, status=status.HTTP_200_OK)

@roles([UserRole.ADMIN])
def create_book(request):
  validated_data = DTOValidator.validate(CreateBookDto, request.data)
  result = book_service.create_book(validated_data, str(request.user.user_id))
  return Response(result, status=status.HTTP_201_CREATED)

def get_book_by_id(request, book_id):
  result = book_service.get_book_by_id(book_id)
  return Response(result, status=status.HTTP_200_OK)

@roles([UserRole.ADMIN])
def update_book(request, book_id):
  validated_data = DTOValidator.validate(UpdateBookDto, request.data)
  result = book_service.update_book(book_id, validated_data)
  return Response(result, status=status.HTTP_200_OK)

@roles([UserRole.ADMIN])
def delete_book(request, book_id):
  book_service.delete_book(book_id)
  return Response({'message': 'Book deleted successfully'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
  method='get',
  operation_summary="Get all books",
  query_serializer=GetBooksDto,
  responses={200: 'List of books'}
)
@swagger_auto_schema(
  method='post',
  operation_summary="Create a new book",
  request_body=CreateBookDto,
  responses={201: 'Book created successfully'}
)
@api_view(['GET', 'POST'])
def books(request):
  if request.method == 'GET':
    return get_books(request)
  else:  # POST
    return create_book(request)

@swagger_auto_schema(
  method='get',
  operation_summary="Get a book by ID",
  responses={200: 'Book details', 404: 'Book not found'}
)
@swagger_auto_schema(
  method='patch',
  operation_summary="Update a book by ID",
  request_body=UpdateBookDto,
  responses={200: 'Updated book details', 404: 'Book not found', 409: 'ISBN conflict'}
)
@swagger_auto_schema(
  method='delete',
  operation_summary="Delete a book by ID (soft delete)",
  responses={200: 'Book deleted successfully', 404: 'Book not found'}
)
@api_view(['GET', 'PATCH', 'DELETE'])
def book_detail(request, book_id):
  if request.method == 'GET':
    return get_book_by_id(request, book_id)
  elif request.method == 'PATCH':
    return update_book(request, book_id)
  else:  # DELETE
    return delete_book(request, book_id)
