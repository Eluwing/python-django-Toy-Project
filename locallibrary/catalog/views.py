from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # books title contain('of', a~z and A~Z)
    num_books_of = Book.objects.filter(title__icontains='of').count()

    # books title contain('of', a~z and A~Z)
    books_title_of = Book.objects.filter(title__icontains='of').get

    # genre name of books title contain('of', a~z and A~Z)
    books_genre_of = Book.objects.filter(title__icontains='of').values('genre')

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_of': num_books_of,
        'books_title_of': books_title_of,
        'books_genre_of': books_genre_of,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView) :
    model = Author
