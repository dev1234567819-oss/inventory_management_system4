"""Simple validation helpers."""


def is_non_empty(*values):
    return all(v is not None and str(v).strip() != "" for v in values)


def is_valid_float(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False
