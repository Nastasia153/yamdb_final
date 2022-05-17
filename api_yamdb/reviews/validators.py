import datetime

from django.core.validators import MaxValueValidator, RegexValidator


def this_year():
    return datetime.date.today().year


def validator_year():
    return MaxValueValidator(
        this_year,
        message='Год выпуска не может быть больше текущего!'
    )


def username_validator():
    return RegexValidator(
        regex=r'^[\w.@+-]+$',
        message='Допускаются буквы, цифры и знаки _ @ / + - .'
    )
