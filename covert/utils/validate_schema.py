import jsonschema
import jsonschema.validators


def validate_schema(schema: dict, data: list[tuple[str, dict]]) -> dict[str, list[str]]:
    """
    Validate a schema against a list of data.
    Args:
        schema: The schema to validate against.
        data: A list of tuples, where the first element is the key and the second element is the data to validate.
    Returns:
        A dictionary where the key is the key from the data and the value is a list of errors.
    """

    validator = jsonschema.validators.validator_for(schema)(
        schema, format_checker=jsonschema.FormatChecker()
    )
    errors = {}
    for key, row in data:
        instance_errors = validate_schema_instance(validator, row)
        if instance_errors:
            errors[key] = instance_errors
    return errors


def validate_schema_instance(validator: jsonschema.Validator, data: dict) -> list[str]:
    try:
        return [str(e) for e in validator.iter_errors(data)]
    except jsonschema.exceptions.ValidationError as e:
        return [str(e)]
