import string

from django.core.exceptions import ValidationError

NUMBER_CAPITALS = 1
NUMBER_SYMBOLS = 1
NUMBER_DIGITS = 1
SYMBOLS = "[~!@#$%^&*()_+{}\":;'[]"


# based on https://stackoverflow.com/questions/67155953/django-auth-password-validators-check-for-symbols-and-other-requirements

class CapitalSymbolDigitValidator:
    def __init__(self):
        self.number_of_capitals = NUMBER_CAPITALS
        self.number_of_symbols = NUMBER_SYMBOLS
        self.number_of_digits = NUMBER_DIGITS
        self.symbols = SYMBOLS
        self.message = "Hasło musi zawierać co najmniej- " + "\n dużych liter: " + str(
            self.number_of_capitals) + '\n symboli: ' + str(
            self.number_of_symbols) + '\n cyfer: ' + str(self.number_of_digits)

    def validate(self, password, user=None):
        capitals = [char for char in password if char.isupper()]
        symbols = [char for char in password if char in self.symbols]
        digits = [char for char in password if char in string.digits]
        if len(capitals) < self.number_of_capitals:
            raise ValidationError(
                self.message,
                code='password_too_short',
                params={'min_length': self.number_of_capitals},
            )
        if len(symbols) < self.number_of_symbols:
            raise ValidationError(
                self.message,
                code='password_too_short',
                params={'min_length': self.number_of_symbols},
            )
        if len(digits) < self.number_of_digits:
            raise ValidationError(
                self.message,
                code='password_too_short',
                params={'min_length': self.number_of_digits},
            )

    def get_help_text(self):
        return self.message
