import random

from django.core.management.base import BaseCommand
from core.models import Author, Book
from faker import Faker


class Command(BaseCommand):

    help = "Initializes database."

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS("Starting fill the database"))

        Author.objects.all().delete()  # will delete all book as cascade

        leo_tolstoy = Author.objects.create(name="Leo Tolstoy")
        alexandre_dumas = Author.objects.create(name="Alexandre Dumas")

        Book.objects.create(title="War and Peace", author=leo_tolstoy)
        Book.objects.create(title="Anna Karenina", author=leo_tolstoy)
        Book.objects.create(title="Resurrection", author=leo_tolstoy)
        Book.objects.create(title="The Three Musketeer", author=alexandre_dumas)
        Book.objects.create(title="The Count of Monte Cristo", author=alexandre_dumas)

        # add some fake data to make the things more interesting
        fake = Faker()
        for _ in range(100):
            new_author = Author.objects.create(name=fake.name())
            books = []
            for _ in range(10):
                fake_book = Book(
                    title=fake.sentence(
                        nb_words=random.choice([2, 4, 5]),
                        variable_nb_words=False
                    ),
                    author=new_author
                )
                books.append(fake_book)
            Book.objects.bulk_create(books)

        self.stdout.write(self.style.SUCCESS(f"Database filled with {Book.objects.all().count()} books"))
