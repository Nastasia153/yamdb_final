from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Category, Comment, Genre, Review, Title, YamdbUser


@admin.register(YamdbUser)
class YamdbUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'role'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Personal info'),
            {'fields': ('first_name', 'last_name', 'email', 'bio')}
        ),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'role', 'is_superuser'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    empty_value_display = '-пусто-'


class GenreInline(admin.TabularInline):
    model = Title.genre.through
    verbose_name = 'связь произведение-жанр'
    verbose_name_plural = 'связи произведение-жанр'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = [GenreInline, ]


class TitleAdminForm(forms.ModelForm):
    class Meta:
        model = Title
        widgets = {
            'name': forms.TextInput()
        }
        fields = '__all__'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    form = TitleAdminForm
    list_display = (
        'id',
        'name',
        'year',
        'category',
        'get_genre'
    )
    search_fields = ('name',)
    list_editable = ('category',)
    empty_value_display = '-пусто-'

    def get_genre(self, obj):
        return ',\n'.join([p.name for p in obj.genre.all()])
    get_genre.short_description = 'жанр'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = ('title__name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date'
    )
