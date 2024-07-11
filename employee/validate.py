from datetime import datetime

from employee.const import DATE_FORMAT


class ValidationError(Exception):
    pass


class ValidateBase:

    def validate(self, name, value):
        raise NotImplementedError

    def raise_exception(self, name, value, exception):
        raise ValidationError(f"Unable to validate {name} with value {value}. Exception: {exception}")


class ValidateID(ValidateBase):

    def validate(self, name, value):
        try:
            assert type(value) is str
            int(value)
        except (ValueError, AssertionError) as exception:
            self.raise_exception(name, value, exception)


class ValidateDateFrom(ValidateBase):

    def validate(self, name, value):
        try:
            assert type(value) is str
            datetime.strptime(value, DATE_FORMAT)
        except (ValueError, AssertionError) as exception:
            self.raise_exception(name, value, exception)


class ValidateDateTo(ValidateBase):

    def validate(self, name, value):
        try:
            assert type(value) is str
            if value and value.lower() != 'null':
                datetime.strptime(value, DATE_FORMAT)
        except (ValueError, AssertionError) as exception:
            self.raise_exception(name, value, exception)


class Validator:

    def __init__(self):
        self.emp_id_validator = ValidateID()
        self.project_id_validator = ValidateID()
        self.date_from_validator = ValidateDateFrom()
        self.date_to_validator = ValidateDateTo()

    def validate(self, emp_id, project_id, date_from, date_to):
        self.emp_id_validator.validate('emp_id', emp_id)
        self.project_id_validator.validate('project_id', project_id)
        self.date_from_validator.validate('date_from', date_from)
        self.date_to_validator.validate('date_to', date_to)
