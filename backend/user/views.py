from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from user.dto.create_user_dto import CreateUserDto
from user.services import UserService
from utils.dto_validator import DTOValidator
from utils.serializer_model import serialize_model

class UserView(APIView):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.user_service = UserService()

  @swagger_auto_schema(
    operation_summary="Create a new user",
    request_body=CreateUserDto,
  )
  def post(self, request):
    validated_data = DTOValidator.validate(CreateUserDto, request.data)
    result = self.user_service.create_user(validated_data)
    return Response(result, status=status.HTTP_201_CREATED)
