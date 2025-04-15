import uuid


def is_uuid(value: str) -> bool:
    """Check if a string value is a valid UUID."""
    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj) == value
    except (ValueError, AttributeError, TypeError):
        return False
