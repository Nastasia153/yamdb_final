"""Модуль загрузки тестовых данных"""
import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Model
from reviews.models import Category, Comment, Genre, Review, Title, User

CSV_DIR = os.path.join(settings.BASE_DIR, 'static/data/')


class Command(BaseCommand):
    help = f'Loads sample data from CSV files in "{CSV_DIR}"'

    def load_csv(self, model: Model, filename: str):
        with open(
            os.path.join(CSV_DIR, filename),
            mode='r', encoding='utf-8', newline=''
        ) as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                params = dict(zip(headers, row))
                if hasattr(model.objects, 'create_user'):
                    model.objects.create_user(**params)
                    continue
                instance = model()
                for key, value in params.items():
                    key_id = f'{key}_id'
                    if hasattr(instance, key_id):
                        setattr(instance, key_id, value)
                    else:
                        setattr(instance, key, value)
                instance.save()

    @transaction.atomic
    def handle(self, *args, **options):
        models = {
            User: 'users',
            Category: 'category',
            Genre: 'genre',
            Title: 'titles',
            Review: 'review',
            Comment: 'comments',
            Title.genre.through: 'genre_title'
        }
        try:
            for model, filebase in models.items():
                self.load_csv(model, f'{filebase}.csv')
        except Exception as error:
            raise CommandError(f'что-то пошло не так. {error}')
