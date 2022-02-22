import logging
from django.http import JsonResponse
from django.conf import settings
from core.models import Author, Book
from core.controllers import ErgeonPaginator
from collections import defaultdict
from core.decorators import endpoint_usage
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("ergon_test")


@endpoint_usage()
@require_http_methods('GET')
@csrf_exempt
def book_title_and_author_name(request):
    """
        [TASK-4.1] Using Django ORM, write a function that will print the book title and the author name (who wrote it)
        for all the books we have in the database. Like this:
        “War and Peace”. Leo Tolstoy
        “Anna Karenina”. Leo Tolstoy
        “Resurrection”. Leo Tolstoy
        “The Three Musketeers”. Alexandre Dumas
        “The Count of Monte Cristo”. Alexandre Dumas
    """
    query_set = Book.objects.filter_book_title_and_author_name()

    """
    SELECT "core_book"."title", "core_author"."name" FROM "core_book"
    INNER JOIN "core_author" ON ("core_book"."author_id" = "core_author"."id")
    ORDER BY "core_author"."name" ASC
    """

    data, object_list = ErgeonPaginator(
        size=int(request.GET.get("size", 50)),
        page=int(request.GET.get("page", 1)),
        query_set=query_set
    ).get_response()

    # normalizing the data to fit in a standard json format
    data["books"] = {title: author for (title, author) in object_list}

    return JsonResponse(data)


@endpoint_usage()
@require_http_methods('GET')
@csrf_exempt
def author_name_and_all_book_titles(request):
    """
    [TASK-4.2] Write another function that will print the author’s name and all the books he wrote.
    For all the authors we have in the database. Like this:
    Leo Tolstoy: “War and Peace”, “Anna Karenina”, “Resurrection”
    Alexandre Dumas: “The Three Musketeers”, “The Count of Monte Cristo”
    """
    query_set = Author.objects.filter_author_name_and_all_book_titles()

    """
    SELECT "core_author"."name", "core_book"."title" FROM "core_author"
    LEFT OUTER JOIN "core_book" ON ("core_author"."id" = "core_book"."author_id")
    ORDER BY "core_author"."name" ASC
    """

    data, object_list = ErgeonPaginator(
        size=int(request.GET.get("size", 50)),
        page=int(request.GET.get("page", 1)),
        query_set=query_set
    ).get_response()

    # normalizing the data to fit in a standard json format
    data["authors"] = defaultdict(list)

    for author, title in object_list:
        data["authors"][author].append(title)

    return JsonResponse(data)


@endpoint_usage()
@require_http_methods('GET')
@csrf_exempt
def author_name_and_book_count(request):

    """
    [TASK-4.3] Implement the third function, it should print the author’s name and the number of books he wrote.
    Order by the number of books written, descending. Like this:
    Leo Tolstoy: 3
    Alexandre Dumas: 2
    """
    query_set = Author.objects.filter_author_name_and_all_book_titles()

    """
    SELECT "core_author"."name", COUNT("core_book"."id") AS "book_count" FROM "core_author"
    LEFT OUTER JOIN "core_book" ON ("core_author"."id" = "core_book"."author_id")
    GROUP BY "core_author"."name" ORDER BY "book_count" DESC
    """

    data, object_list = ErgeonPaginator(
        size=int(request.GET.get("size", 50)),
        page=int(request.GET.get("page", 1)),
        query_set=query_set
    ).get_response()

    # normalizing the data to fit in a standard json format
    data["authors"] = {author: count for (author, count) in object_list}

    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def button_counter(request):

    if request.method == "GET":
        total_count = settings.REDIS.get("button_counter") or 0
    else:
        total_count = settings.REDIS.incr("button_counter")

    if not isinstance(total_count, int):
        total_count = int(total_count)

    return JsonResponse({'total_count': total_count})
