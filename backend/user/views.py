from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from user.dto.create_user_dto import CreateUserDto
from dto.email_password_dto import EmailPasswordDto
from user.services import UserService
from utils.dto_validator import DTOValidator
from decorators.is_public import is_public

user_service = UserService()

@swagger_auto_schema(
  method='post',
  operation_summary="Create a new user",
  request_body=CreateUserDto,
)
@is_public
@api_view(['POST'])
def create_user(request):
  validated_data = DTOValidator.validate(CreateUserDto, request.data)
  result = user_service.create_user(validated_data)
  return Response(result, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
  method='post',
  operation_summary="Login user",
  request_body=EmailPasswordDto,
)
@is_public
@api_view(['POST'])
def login(request):
  validated_data = DTOValidator.validate(EmailPasswordDto, request.data)
  result = user_service.login(validated_data)
  return Response(result, status=status.HTTP_200_OK)
