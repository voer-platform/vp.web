
from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(u'%s is not an even number' % value)


def validate_required(value):
    if value == "" or value is None:
        raise ValidationError(u'Value is required')