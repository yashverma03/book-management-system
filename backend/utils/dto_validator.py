from rest_framework import serializers
from utils.exceptions import BadRequestException


class DTOValidator:
    """
    Utility class to validate DTOs and automatically raise BadRequestException
    if validation fails
    """

    @staticmethod
    def validate(dto_class: type[serializers.Serializer], data: dict) -> dict:
        """
        Validate data against a DTO class

        Args:
            dto_class: The DTO serializer class to validate against
            data: The data dictionary to validate

        Returns:
            dict: Validated data

        Raises:
            BadRequestException: If validation fails
        """
        dto = dto_class(data=data)

        if not dto.is_valid():
            raise BadRequestException(
                detail='Bad Request Exception',
                error=dto.errors
            )

        return dto.validated_data
