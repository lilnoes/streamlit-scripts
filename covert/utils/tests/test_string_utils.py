import pytest
from covert.utils.string_utils import is_uuid, extract_uuid


@pytest.mark.parametrize(
    "uuid_str, valid",
    [
        ("123e4567-e89b-12d3-a456-426614174000", True),
        ("not-a-uuid", False),
        ("123e4567-e89b-12d3-a456-42661417400", False),
    ],
)
def test_uuid_validation(uuid_str: str, valid: bool):
    assert is_uuid(uuid_str) == valid


def test_extract_single_uuid():
    # Test extracting a single UUID from text
    text = "This is a UUID: 123e4567-e89b-12d3-a456-426614174000 in some text."
    result = extract_uuid(text)

    assert len(result) == 1
    assert result[0] == "123e4567-e89b-12d3-a456-426614174000"


def test_extract_multiple_uuids():
    # Test extracting multiple UUIDs from text
    text = """
    First UUID: 123e4567-e89b-12d3-a456-426614174000
    Second UUID: 00000000-0000-0000-0000-000000000000
    Third UUID: ffffffff-ffff-ffff-ffff-ffffffffffff
    Fourth invalid UUID: ffffff-ffff-ffff-ffff-ffffffffffff
    """
    result = extract_uuid(text)

    assert len(result) == 3
    assert "123e4567-e89b-12d3-a456-426614174000" in result
    assert "00000000-0000-0000-0000-000000000000" in result
    assert "ffffffff-ffff-ffff-ffff-ffffffffffff" in result


def test_extract_concatenated_uuids():
    """
    Test extracting a single UUID from text that is concatenated with other text.
    """
    text = "123e4567-e89b-12d3-a456-4266141740000000-0000-0000-0000-000000000000"
    result = extract_uuid(text)

    assert len(result) == 1
    assert "123e4567-e89b-12d3-a456-426614174000" in result
