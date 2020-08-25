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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_of': num_books_of,
        'books_title_of': books_title_of,
        'books_genre_of': books_genre_of,
        'num_visits': num_visits,
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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksByLlibrarianListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    # permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author')

@permission_required('catalog.can_mark_returned')
class ManageAuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('manage-author')

@permission_required('catalog.can_mark_returned')
class ManageAuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('manage-author')

@permission_required('catalog.can_mark_returned')
class ManageAuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('manage-author')

@permission_required('catalog.can_mark_returned')
class ManageBookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('manage-book')

@permission_required('catalog.can_mark_returned')
class ManageBookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('manage-book')

@permission_required('catalog.can_mark_returned')
class ManageBookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('manage-book')

class ManagementBookListView(generic.ListView):
    model = Book
    template_name = 'catalog/manage_book_list.html'
    paginate_by = 5

class ManagementAuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/manage_author_list.html'
    paginate_by = 5
