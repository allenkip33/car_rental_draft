from datetime import date


def validate_date(date_text):
    try:
        date.fromisoformat(date_text)
        return True
    except ValueError:
        return False


def validate_future_date(date_text):
    if not validate_date(date_text):
        return False
    return date.fromisoformat(date_text) >= date.today()


def validate_date_range(start_date_text, end_date_text):
    if not validate_date(start_date_text) or not validate_date(end_date_text):
        return False
    return date.fromisoformat(end_date_text) > date.fromisoformat(start_date_text)


def validate_price(price):
    try:
        return float(price) > 0
    except (ValueError, TypeError):
        return False


def validate_year(year_text, min_year=1900):
    try:
        year = int(year_text)
    except (ValueError, TypeError):
        return False
    return min_year <= year <= date.today().year + 1


def validate_required(value):
    return bool(value and value.strip())
