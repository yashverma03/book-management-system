from django.db import models
from django.utils import timezone
import uuid


def serialize_model(instance):
    """
    Generic function to serialize any Django model instance to JSON-serializable dictionary

    Args:
        instance: Django model instance

    Returns:
        dict: Serialized model data
    """
    data = {}

    # Get all fields from the model
    for field in instance._meta.get_fields():
        field_name = field.name

        # Skip reverse relations (ForeignKey reverse, ManyToMany reverse)
        if field.one_to_many or field.many_to_many:
            continue

        try:
            value = getattr(instance, field_name)

            # Handle different field types
            if value is None:
                data[field_name] = None
            elif isinstance(field, models.UUIDField):
                data[field_name] = str(value)
            elif isinstance(field, (models.DateTimeField, models.DateField, models.TimeField)):
                if value:
                    data[field_name] = value.isoformat()
                else:
                    data[field_name] = None
            elif isinstance(field, models.ForeignKey):
                # For ForeignKey, serialize the related object's ID
                if value:
                    if hasattr(value, 'id'):
                        data[field_name] = str(value.id) if isinstance(value.id, uuid.UUID) else value.id
                    else:
                        data[field_name] = str(value)
                else:
                    data[field_name] = None
            elif isinstance(field, models.BooleanField):
                data[field_name] = bool(value)
            elif isinstance(field, models.IntegerField):
                data[field_name] = int(value) if value is not None else None
            elif isinstance(field, models.FloatField):
                data[field_name] = float(value) if value is not None else None
            elif isinstance(field, models.DecimalField):
                data[field_name] = float(value) if value is not None else None
            else:
                # For CharField, TextField, EmailField, etc., convert to string
                data[field_name] = str(value) if value is not None else None

        except AttributeError:
            # Skip fields that don't exist or can't be accessed
            continue

    return data
