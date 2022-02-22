from django.db import models


class AuthorQuerySet(models.QuerySet):

    def filter_author_name_and_all_book_titles(self):
        return Author.objects.all().values_list("name", "book__title").order_by("name")

    def filter_author_name_and_book_count(self):
        return Author.objects.all().values_list('name').annotate(
            book_count=models.Count('book')
        ).order_by('-book_count')


class BookQuerySet(models.QuerySet):

    def filter_book_title_and_author_name(self):
        return Book.objects.select_related("author").all().order_by("author__name").values_list("title", "author__name")


class Author(models.Model):
    name = models.CharField(max_length=100)
    objects = AuthorQuerySet.as_manager()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    objects = BookQuerySet.as_manager()
