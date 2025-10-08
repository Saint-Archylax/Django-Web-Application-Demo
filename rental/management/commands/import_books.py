import json
from django.core.management.base import BaseCommand
from rental.models import Book, BookCopy
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Import books from JSON with created_at override and auto-generate copies'

    def handle(self, *args, **kwargs):
        try:
            with open('rental/fixtures/books_fixture.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Fixture file not found.'))
            return

        count = 0
        skipped = 0

        for entry in data:
            fields = entry.get('fields', {})
            created_at_str = fields.pop('created_at', None)
            created_at = parse_datetime(created_at_str) if created_at_str else now()

            copies = entry.get('copies', 3)  # default to 3 if not specified

            try:
                book = Book(**fields)
                book.created_at = created_at
                book.save()

                for i in range(1, copies + 1):
                    BookCopy.objects.create(book=book, copy_number=i, status='available')

                count += 1
            except Exception as e:
                skipped += 1
                self.stdout.write(self.style.WARNING(f'Skipped book with ISBN {fields.get("isbn")}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Imported {count} books successfully.'))
        if skipped:
            self.stdout.write(self.style.WARNING(f'Skipped {skipped} entries due to errors.'))