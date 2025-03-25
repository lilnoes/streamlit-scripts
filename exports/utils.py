import re
from sympy import sympify
from sympy.parsing.latex import parse_latex


def validate_text(text):
    if not text:
        return False, False, "No text to validate"

    try:
        # Define inline LaTeX delimiters patterns
        INLINE_DELIMITERS = [(r"^\$", r"\$$"), (r"^\\\(", r"\\\)$")]

        # Remove inline latex delimiters if present
        text = text.strip()
        for start_pattern, end_pattern in INLINE_DELIMITERS:
            if re.match(start_pattern, text) and re.search(end_pattern, text):
                text = re.sub(start_pattern, "", text)
                text = re.sub(end_pattern, "", text)
                break

        parsed = parse_latex(text, strict=True)
        value = sympify(parsed)
        return True, value.is_number, ""
    except Exception as e:
        return False, False, str(e)


def extract_math_expressions(text: str, inline_only: bool = False) -> list[str]:
    # Regular expressions for detecting LaTeX math delimiters
    INLINE_MATH_REGEX = r"(?<!\\)(?:\$(?!\$)[\s\S]*?(?<!\\)\$(?!\$)|\\\([\s\S]*?\\\))"
    BLOCK_MATH_REGEX = r"(?<!\\)(?:\$\$[\s\S]*?(?<!\\)\$\$|\\\[[\s\S]*?\\\])"

    # Patterns for the delimiters to remove
    BLOCK_DELIMITERS = [(r"^\$\$", r"\$\$$"), (r"^\\\[", r"\\\]$")]
    INLINE_DELIMITERS = [(r"^\$", r"\$$"), (r"^\\\(", r"\\\)$")]

    # Find all math expressions
    all_math = re.findall(f"{BLOCK_MATH_REGEX}|{INLINE_MATH_REGEX}", text)

    # Remove delimiters from each expression
    cleaned_expressions = []
    for expr in all_math:
        # Try block delimiters first
        if not inline_only:
            for start, end in BLOCK_DELIMITERS:
                if re.search(start, expr) and re.search(end, expr):
                    cleaned = re.sub(f"{start}|{end}", "", expr)
                    cleaned_expressions.append(cleaned)
                    break
        else:
            # If not block math, try inline delimiters
            for start, end in INLINE_DELIMITERS:
                if re.search(start, expr) and re.search(end, expr):
                    cleaned = re.sub(f"{start}|{end}", "", expr)
                    cleaned_expressions.append(cleaned)
                    break

    return cleaned_expressions


def extract_all_text(data) -> str:
    """
    Recursively extract text from any data structure and join with spaces.

    Args:
        data: Any Python object (str, list, dict, etc.)

    Returns:
        str: All text content joined with spaces
    """
    result = []

    # Base case: strings are returned directly
    if isinstance(data, str):
        return data

    # Handle lists, tuples, and other iterables
    elif isinstance(data, (list, tuple, set)):
        for item in data:
            result.append(extract_all_text(item))

    # Handle dictionaries - extract from both keys and values
    elif isinstance(data, dict):
        for key, value in data.items():
            result.append(extract_all_text(key))
            result.append(extract_all_text(value))

    # Handle other objects by converting to string if possible
    else:
        try:
            return str(data)
        except:
            return ""

    # Join all extracted text with spaces
    return " ".join(filter(None, result))
