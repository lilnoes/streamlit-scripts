import enum


class FileType(str, enum.Enum):
    JSONL = "jsonl"
    CSV = "csv"
    JSON = "json"
