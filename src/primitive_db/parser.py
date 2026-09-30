import ast


def parse_value(value):
    value = value.strip()

    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False

        return value


def parse_condition(tokens):
    if len(tokens) != 3 or tokens[1] != "=":
        raise ValueError("Некорректное условие")

    column = tokens[0]
    value = parse_value(tokens[2])

    return {column: value}


def parse_values(values_text):
    values = []

    for value in values_text.split(","):
        values.append(parse_value(value))

    return values