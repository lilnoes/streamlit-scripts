import re
from sympy import sympify
from sympy.parsing.latex import parse_latex, parse_latex_lark
from pylatexenc.latex2text import LatexNodes2Text
from covert.scripts.types.parse_type import ParseType
from typing import Any


def validate_text_pylatexenc(text: str) -> tuple[bool, bool, str]:
    if not text:
        return False, False, "No text to validate"

    try:
        LatexNodes2Text().latex_to_text(text)
        return True, False, ""
    except Exception as e:
        return False, False, str(e)


def validate_text_lark(text: str) -> tuple[bool, bool, str]:
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

        parse_latex_lark(text)
        return True, False, ""
    except Exception as e:
        return False, False, str(e)


def validate_text_antlr(text: str) -> tuple[bool, bool, str]:
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


def validate_text(
    text: str, parse_type: ParseType = ParseType.SYMPY_ANTLR
) -> tuple[bool, bool, str]:
    if parse_type == ParseType.PYLATEXENC:
        return validate_text_pylatexenc(text)
    elif parse_type == ParseType.SYMPY_LARK:
        return validate_text_lark(text)
    elif parse_type == ParseType.SYMPY_ANTLR:
        return validate_text_antlr(text)

    else:
        raise ValueError(f"Invalid parse type: {parse_type}")


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


def extract_all_text(data: Any) -> str:
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
