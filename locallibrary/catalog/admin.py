from django.contrib import admin
from django.utils.html import format_html

from .models import Author, Book, BookInstance, Genre, Language

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")

    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")

    def display_genre(self, obj):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ", ".join(genre.name for genre in obj.genre.all()[:3])

    display_genre.short_description = "Genre"


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "borrower", "due_back", "id")
    list_filter = ("status", "due_back")

    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )

    def display_book_details(self, obj):
        if not obj.book:
            return "No book assigned"
        genre = (
            obj.book.display_genre() if hasattr(obj.book, "display_genre") else "N/A"
        )
        summary = obj.book.summary if hasattr(obj.book, "summary") else "N/A"
        return format_html(
            "<strong>Genre:</strong> {}<br><strong>Summary:</strong> {}", genre, summary
        )

    display_book_details.short_description = "Book Details"

    def book_details_for_list(self, obj):
        if not obj.book:
            return "No book"
        return (
            f"Genre: {obj.book.display_genre()} \n Summary: {obj.book.summary[:50]}..."
        )

    book_details_for_list.short_description = "Book Details (List)"


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")

    inlines = [BooksInstanceInline]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Language)
