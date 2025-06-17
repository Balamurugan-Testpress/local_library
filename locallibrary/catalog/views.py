from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_visited = request.session.get("num_visited", 0)
    num_visited = num_visited + 1
    request.session["num_visited"] = num_visited
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    num_authors = Author.objects.count()

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_visited": num_visited,
    }
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 1


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksByLibrarianListView(LoginRequiredMixin, generic.ListView):
    """View listing all books on loan — visible only to librarians."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_books.html"
    paginate_by = 10

    def get_queryset(self):
        # Only show books currently on loan
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")

    def test_func(self):
        # Only allow users in 'Librarians' group
        return self.request.user.groups.filter(name="Librarians").exists()

    def get_context_data(self, **kwargs):
        # Add 'is_librarian' to context for use in the template
        context = super().get_context_data(**kwargs)
        context["is_librarian"] = self.request.user.groups.filter(
            name="Librarians"
        ).exists()
        return context
