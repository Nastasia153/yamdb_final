from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import username_validator, validator_year


class PrintFieldMixin:
    """Печать заданного поля с учетом ограничений"""
    def __str__(self):
        if hasattr(self, 'text'):
            return self.text[:settings.REVIEW['LENGTH_LIMIT']]
        if hasattr(self, 'name'):
            return self.name[:settings.REVIEW['LENGTH_LIMIT']]
        return super().__str__()


class YamdbUser(AbstractUser):
    """Модель пользователя Yamdb"""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLES = (
        (USER, 'пользователь'),
        (ADMIN, 'админ'),
        (MODERATOR, 'модератор')
    )

    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        validators=(username_validator(),)
    )
    email = models.EmailField('электронная почта', max_length=254, unique=True)
    first_name = models.CharField(
        'имя',
        max_length=150,
        null=True, blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        null=True, blank=True
    )
    bio = models.TextField('о себе', null=True, blank=True)
    role = models.CharField(
        'роль',
        max_length=max(len(key) for key, _ in ROLES),
        choices=ROLES,
        default=USER
    )
    code = models.CharField(max_length=20, null=True, blank=True)

    @property
    def is_admin(self):
        return (
            self.is_staff
            or self.role == YamdbUser.ADMIN
        )


User = get_user_model()


class RubricBase(PrintFieldMixin, models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='код',
        max_length=50
    )

    class Meta:
        abstract = True
        ordering = ('name',)


class Category(RubricBase):

    class Meta(RubricBase.Meta):
        default_related_name = 'categories'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Genre(RubricBase):

    class Meta(RubricBase.Meta):
        default_related_name = 'genres'
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(PrintFieldMixin, models.Model):
    name = models.TextField(
        verbose_name='название'
    )
    year = models.SmallIntegerField(
        validators=[validator_year()],
        verbose_name='год выпуска'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='описание'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='категория'
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        # ordering = ('name',) # не работает с версии 3.1 при annotate


class BaseInfo(PrintFieldMixin, models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='дата добавления'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    # def __str__(self):
    #     return self.text[:settings.REVIEW['LENGTH_LIMIT']]


class Review(BaseInfo):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='название')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Не меньше 1'),
            MaxValueValidator(10, message='Не больше 10')
        ],
        verbose_name='оценка',
        default=1
    )

    class Meta(BaseInfo.Meta):
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )]
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class Comment(BaseInfo):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='отзыв'
    )

    class Meta(BaseInfo.Meta):
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
