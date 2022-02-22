## ERGEON test for Ademar Victorino

### Olá developer. 

A django application with some views methods was created to implement some related functionality to the test in a more realistic format.
I'm providing a dockerfile for the backend and another for the front, so you can run it in your local environment.
Since the database is hosted on heroku the .env will be sent by email to not leave passwords on github.

I used a REDIS instance (heroku) to optimize the click count function.
REDIS offers the perfect solution: INCR https://redis.io/commands/INCR 
 
### Task 1: 
##### Global Interpreter locker
 - Protect the access to python objects
 - Prevents multiple threads from execution python bytecode at once
 - Prevents multithread applications from taking advantage of multiprocessing systems,
 - Is a no real parallel computing 
 - We can use parallel process but it is not efficient as threads


### Task 2:
Have a look into `/core/decorators/enpoint_usage.py` file, have the simplest usage of a decorator. 
Also created another one called `LastQueryLogger`, few free to have a look at.

### Task 3
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

### Task 4
As I said before, I created a small app to represent the queries. 
You can find all implementation in the views file that answers each endpoint. 
I added some pagination features to make it easy to load all data in a frontend (`core/controllers/ergeon_paginator.py`)

#### 4.1
`core.views.book_title_and_author_name` with the query was implemented as a QuerySet extension:
```
Book.objects.select_related("author").all().order_by("author__name").values_list("title", "author__name")

SELECT "core_book"."title", "core_author"."name" FROM "core_book"
    INNER JOIN "core_author" ON ("core_book"."author_id" = "core_author"."id")
    ORDER BY "core_author"."name" ASC
```
#### 4.2
`core.views.author_name_and_all_book_titles` with the query was implemented as a QuerySet Extension:
```      
Author.objects.all().values_list("name", "book__title").order_by("name")
    
SELECT "core_author"."name", "core_book"."title" FROM "core_author"
    LEFT OUTER JOIN "core_book" ON ("core_author"."id" = "core_book"."author_id")
    ORDER BY "core_author"."name" ASC
```
#### 4.3
`core.views.author_name_and_book_count` with the query was implemented as a QuerySet Extension:
```
Author.objects.all().values_list('name').annotate(
        book_count=models.Count('book')
    ).order_by('-book_count')

SELECT "core_author"."name", COUNT("core_book"."id") AS "book_count" FROM "core_author"
    LEFT OUTER JOIN "core_book" ON ("core_author"."id" = "core_book"."author_id")
    GROUP BY "core_author"."name" ORDER BY "book_count" DESC
```

### Task 5
- Regular functions may have a name or exist without a name. The arrow always is anonymous.
- Regular functions could be hoisted ( declared in scope and called before it ), arrows functions is not possible because is anonymous, but you can assign a function to a variable LET/CONST
- Anonimous doesn't have "This" the variable will take from the outer scope or global / window

### Task 6
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

