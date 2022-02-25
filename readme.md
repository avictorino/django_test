## Test for Ademar Victorino

### Hi developer. 

A django application with some views methods was created to implement some related functionality to the test in a more realistic format.
I'm providing a dockerfile for the backend and another for the front, so you can run it in your local environment.
Since the database is hosted on heroku the .env will be sent by email to not leave passwords on github.

I used a REDIS instance (heroku) to optimize the click count function.
REDIS offers the perfect solution: INCR https://redis.io/commands/INCR 
 
### Task 1 - Describe in your own words what is GIL in python, and the pros and cons of it.
Global Interpreter locker
 - Protect the access to python objects
 - Prevents multiple threads from execution python bytecode at once
 - Prevents multithread applications from taking advantage of multiprocessing systems,
 - Is a no real parallel computing 
 - We can use parallel process but it is not efficient as threads


### Task 2 - Write a decorator in python that will count how many times the decorated function was called. It should print the number every time the decorated function is executed. Each function should be counted separately.

Have a look into `/core/decorators/enpoint_usage.py` file, have the simplest usage of a decorator. 
Also created another one called `LastQueryLogger`, few free to have a look at.

### Task 3 - If you see that a SQL SELECT query is slow - what would you do to improve it?
The first approach is to execute the query using the EXPLAIN in order to show the execution plan of a statement.

```
EXPLAIN
SELECT "core_author"."name", "core_book"."title" FROM "core_author" 
        LEFT OUTER JOIN "core_book" ON ("core_author"."id" = "core_book"."author_id") 
        ORDER BY "core_author"."name" asc

QUERY PLAN                                                                    |
------------------------------------------------------------------------------+
Sort  (cost=75.21..77.72 rows=1005 width=38)                                  |
  Sort Key: core_author.name                                                  |
  ->  Hash Right Join  (cost=3.29..25.09 rows=1005 width=38)                  |
        Hash Cond: (core_book.author_id = core_author.id)                     |
        ->  Seq Scan on core_book  (cost=0.00..19.05 rows=1005 width=32)      |
        ->  Hash  (cost=2.02..2.02 rows=102 width=22)                         |
              ->  Seq Scan on core_author  (cost=0.00..2.02 rows=102 width=22)|
```

You can see the 'Hash Cond'is the most important condition in the execution plan describing the path that the query is doing to apply the joins.
Make sure all joint columns are indexed using biginteger datatypes. 
The disadvantage to having multiple indexed fields is the insert delay caused by the index regeneration.

The other approach is to denormalize the table... let this for another conversation.

### Task 4 Let’s say we have the following models in Django project:

```
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

Leo_tolstoy = Author.objects.create(name=”Leo Tolstoy”)
alexandre_dumas = Author.objects.create(name=”Alexandre Dumas”)
Book.objects.create(title=”War and Peace”, author=leo_tolstoy)
Book.objects.create(title=”Anna Karenina”, author=leo_tolstoy)
Book.objects.create(title=”Resurrection”, author=leo_tolstoy)
Book.objects.create(title=”The Three Musketeer”, author=alexandre_dumas)
Book.objects.create(title=”The Count of Monte Cristo”, author=alexandre_dumas)
```
Assume we have ~100 books and ~25 authors in our database.
Try to write efficient queries, keep in mind how many requests the ORM can make to the database.

##### 4.1 Using Django ORM, write a function that will print the book title and the author name (who wrote it) for all the books we have in the database. Like this:

“War and Peace”. Leo Tolstoy
“Anna Karenina”. Leo Tolstoy
“Resurrection”. Leo Tolstoy
“The Three Musketeers”. Alexandre Dumas
“The Count of Monte Cristo”. Alexandre Dumas


`core.views.book_title_and_author_name` with the query was implemented as a QuerySet extension:
```
Book.objects.select_related("author").all().order_by("author__name").values_list("title", "author__name")

SELECT "core_book"."title", "core_author"."name" FROM "core_book"
    INNER JOIN "core_author" ON ("core_book"."author_id" = "core_author"."id")
    ORDER BY "core_author"."name" ASC
```

##### 4.2 Write another function that will print the author’s name and all the books he wrote. For all the authors we have in the database. Like this:

Leo Tolstoy: “War and Peace”, “Anna Karenina”, “Resurrection”
Alexandre Dumas: “The Three Musketeers”, “The Count of Monte Cristo”


`core.views.author_name_and_all_book_titles` with the query was implemented as a QuerySet Extension:
```      
Author.objects.all().values_list("name", "book__title").order_by("name")
    
SELECT "core_author"."name", "core_book"."title" FROM "core_author"
    LEFT OUTER JOIN "core_book" ON ("core_author"."id" = "core_book"."author_id")
    ORDER BY "core_author"."name" ASC
```

#### 4.3 Implement the third function, it should print the author’s name and the number of books he wrote. Order by the number of books written, descending. Like this:

Leo Tolstoy: 3
Alexandre Dumas: 2

`core.views.author_name_and_book_count` with the query was implemented as a QuerySet Extension:
```
Author.objects.all().values_list('name').annotate(
        book_count=models.Count('book')
    ).order_by('-book_count')

SELECT "core_author"."name", COUNT("core_book"."id") AS "book_count" FROM "core_author"
    LEFT OUTER JOIN "core_book" ON ("core_author"."id" = "core_book"."author_id")
    GROUP BY "core_author"."name" ORDER BY "book_count" DESC
```

### Task 5 What are the differences between “arrow” and “traditional” functions in javascript?
- Regular functions may have a name or exist without a name. The arrow always is anonymous.
- Regular functions could be hoisted ( declared in scope and called before it ), arrows functions is not possible because is anonymous, but you can assign a function to a variable LET/CONST
- Anonimous doesn't have "This" the variable will take from the outer scope or global / window

### Task 6 Write a basic React component showing number of clicks on it’s button, use images below as example, allow to configure initial value of click count.
I added the react application into the client directory ( not is usual in a real-world project )
Inside the component ButtonCounter.js, I added an API request to the backend in order to count the clicks in a single thread, scalable and centralized way.
Using Redis to increment the client we can ensure that all clicks will be registered in a multithread environment.


### Extras
- Dockerfile and compose 
- Redis INCR
- Views and admin
- Frontend integrated with backend using rest GET/PUT
- Database query logging system as decorator `core/decorators/query_logger.py`
- Django management command to fill the database using bulk queries
- Simple admin to inspect/search/edit the data
- Django Queryset extension 
- Sorry no tests, next time I can make the best ones
- Simple Paginator esxtension `core/controllers/ergeon_paginator.py
- Flake8 to make the code clean easy to read 


### Final
> The Github repository and all code will be deleted in a week, no names and references of my name or Ergeon will exist in a few days.

