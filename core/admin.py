from django.contrib import admin
from core.models import Author, Book


class BookAdminInline(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ['name', 'count']
    inlines = [BookAdminInline]

    def count(self, obj):
        return obj.book_set.all().count()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ['title', 'author']
