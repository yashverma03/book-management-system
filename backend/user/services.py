import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from user.models import User
from django.utils import timezone as django_timezone
from utils.exceptions import ConflictException, NotFoundException, UnauthorizedException
from user.serializers import UserSerializer

class UserService:
  def create_user(self, dto):
    existing_user = self.get_user_by_email(dto['email'])
    if existing_user:
      raise ConflictException('User with this email already exists')
    dto['password'] = self.hash_password(dto['password'])
    user = User.objects.create(**dto)
    token = self.generate_token(user)
    user_data = UserSerializer(user).data
    return {
      'token': token,
      'user': user_data,
    }

  def generate_token(self, user) -> str:
    """
    Generate JWT token for user

    Args:
        user: User model instance

    Returns:
        str: JWT token string
    """
    now = datetime.now(timezone.utc)
    payload = {
      'user_id': str(user.id),
      'email': user.email,
      'role': user.role,
      'is_active': True,
      'iat': now,
      'exp': now + timedelta(days=settings.JWT_EXPIRY_DAYS)
    }
    token = jwt.encode(
      payload,
      settings.JWT_SECRET_KEY,
      algorithm='HS256'
    )
    return token

  def hash_password(self, password) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(10)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

  def verify_password(self, password: str, hashed_password: str) -> bool:
    """
    Verify password against hashed password

    Args:
        password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        bool: True if password matches, False otherwise
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

  def login(self, dto):
    """
    Login user with email and password

    Args:
        dto: Dictionary with 'email' and 'password'

    Returns:
        dict: Dictionary with 'token' and 'user' (without password)

    Raises:
        UnauthorizedException: If user not found or password is incorrect
    """
    email = dto['email']
    password = dto['password']

    # Check if user exists
    user = self.get_user_by_email(email)
    if not user:
      raise NotFoundException('User not found')

    # Verify password
    if not self.verify_password(password, user.password):
      raise UnauthorizedException('Invalid email or password')

    # Generate token
    token = self.generate_token(user)

    # Serialize user (password is already excluded in UserSerializer)
    user_data = UserSerializer(user).data

    return {
      'token': token,
      'user': user_data,
    }

  def get_user_by_email(self, email):
    try:
      user = User.objects.only('id', 'email', 'name', 'password', 'role').get(email=email, deleted_at=None)
      return user
    except User.DoesNotExist:
      return None

  def get_user_by_id(self, id):
    try:
      user = User.objects.get(id=id, deleted_at=None)
      return user
    except User.DoesNotExist:
      raise NotFoundException('User not found')

  def get_all_users(self):
    users = User.objects.filter(deleted_at=None)
    return users

  def delete_user(self, id) -> None:
    updated_count = User.objects.filter(
      id=id,
      deleted_at=None
    ).update(deleted_at=django_timezone.now())

    if updated_count == 0:
      raise NotFoundException('User not found or already deleted')
