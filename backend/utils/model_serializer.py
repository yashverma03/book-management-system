from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json


def model_to_dict(model_instance):
    """
    Convert a Django model instance to a dictionary.
    Handles ForeignKey relationships by recursively serializing related objects.

    Args:
        model_instance: Django model instance

    Returns:
        dict: Dictionary representation of the model
    """
    data = {}

    # Get all field names from the model
    for field in model_instance._meta.get_fields():
        field_name = field.name

        # Skip reverse relations
        if field.one_to_many or (field.many_to_many and not field.through):
            continue

        # Handle ForeignKey and OneToOneField
        if field.many_to_one or field.one_to_one:
            related_obj = getattr(model_instance, field_name, None)
            if related_obj:
                # If it's a related object, serialize it recursively
                if isinstance(related_obj, models.Model):
                    data[field_name] = model_to_dict(related_obj)
                else:
                    data[field_name] = related_obj
            elif hasattr(model_instance, f'{field_name}_id'):
                # Store the foreign key ID if related object is not loaded
                data[f'{field_name}_id'] = getattr(model_instance, f'{field_name}_id', None)
        elif field.many_to_many:
            # Skip many-to-many for now
            continue
        else:
            # Regular field
            try:
                value = getattr(model_instance, field_name, None)

                # Handle special types
                if isinstance(value, models.Model):
                    # Nested model - serialize it
                    data[field_name] = model_to_dict(value)
                elif hasattr(value, '__iter__') and not isinstance(value, (str, bytes)):
                    # Skip iterables except strings
                    continue
                else:
                    # Convert to JSON-serializable format
                    try:
                        json.dumps(value, cls=DjangoJSONEncoder)
                        data[field_name] = value
                    except (TypeError, ValueError):
                        # If not JSON serializable, convert to string
                        data[field_name] = str(value) if value is not None else None
            except AttributeError:
                # Skip fields that don't exist or can't be accessed
                continue

    return data
