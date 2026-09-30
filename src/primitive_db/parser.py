def parse_value(value):
    """Parse a string value into a Python value."""
    value = value.strip()

    if value.lower() == "true":
        return True

    if value.lower() == "false":
        return False

    try:
        return int(value)
    except ValueError:
        return value.strip('"').strip("'")


def parse_condition(tokens):
    """Parse a condition into a dictionary."""
    if len(tokens) != 3 or tokens[1] != "=":
        raise ValueError("Некорректное условие")

    column = tokens[0]
    value = parse_value(tokens[2])

    return {column: value}


def parse_values(values_text):
    """Parse comma-separated values into Python values."""
    values = []

    for value in values_text.split(","):
        values.append(parse_value(value))

    return values