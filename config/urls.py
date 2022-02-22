"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import (
    book_title_and_author_name,
    author_name_and_all_book_titles,
    author_name_and_book_count,
    button_counter,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('book-title-and-author-name/', book_title_and_author_name),
    path('author-name-and-all-book-titles/', author_name_and_all_book_titles),
    path('author-name-and-book-count/', author_name_and_book_count),
    path('button-counter/', button_counter)
]
