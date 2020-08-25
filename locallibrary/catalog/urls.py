from django.urls import path
from catalog import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksByLlibrarianListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

    # Admin Management Generic Edit View Page URLS
    path('author/create/', views.ManageAuthorCreate.as_view(), name='manage-author-create'),
    path('author/<int:pk>/update/', views.ManageAuthorUpdate.as_view(), name='manage-author-update'),
    path('author/<int:pk>/delete/', views.ManageAuthorDelete.as_view(), name='manage-author-delete'),

    path('book/create/', views.ManageBookCreate.as_view(), name='manage-book-create'),
    path('book/<int:pk>/update/', views.ManageBookUpdate.as_view(), name='manage-book-update'),
    path('book/<int:pk>/delete/', views.ManageBookDelete.as_view(), name='manage-book-delete'),

    # Admin Management All Output Page URLS
    path('manage-book/', views.ManagementBookListView.as_view(), name='manage-book'),
    path('manage-author/', views.ManagementAuthorListView.as_view(), name='manage-author'),
]
