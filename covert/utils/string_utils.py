import uuid
import re


def is_uuid(value: str) -> bool:
    """Check if a string value is a valid UUID."""
    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj) == value
    except (ValueError, AttributeError, TypeError):
        return False


def extract_uuid(text: str) -> list[str]:
    """Extract all UUIDs from a given text."""
    UUID_PATTERN = (
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    )
    return [match.group(0) for match in re.finditer(UUID_PATTERN, text)]
