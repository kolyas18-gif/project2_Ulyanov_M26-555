def parse_value(value):
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]

    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    if value == "True":
        return True

    if value == "False":
        return False

    try:
        return int(value)
    except ValueError:
        raise ValueError("Некорректное значение")


def parse_condition(condition):
    key, value = condition.split("=", 1)
    key = key.strip()
    value = value.strip()

    return {key: parse_value(value)}


def parse_where(condition):
    return parse_condition(condition)


def parse_set(condition):
    return parse_condition(condition)