import re

from datetime import datetime

from employee.const import ALLOWED_EXTENSIONS, DATE_REGEX, DATE_FORMATS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def prepare_date(date):
    date_regex = re.compile(DATE_REGEX, re.I | re.S)

    match_date = date_regex.search(date)

    if not match_date:
        raise ValueError("Date format not found.")

    return "-".join(match_date.groups())


def make_date(date):
    latest_known_error = None
    formatted_date = None

    prepared_date = prepare_date(date)

    for date_format in DATE_FORMATS:
        try:
            formatted_date = datetime.strptime(prepared_date, date_format)
        except ValueError as exception:
            latest_known_error = exception
            continue

    if formatted_date is None:
        if latest_known_error is not None:
            raise latest_known_error
        raise ValueError(f"Unable to format the date: {prepared_date}")

    return formatted_date
