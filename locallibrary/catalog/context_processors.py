# yourapp/context_processors.py


# yourapp/context_processors.py


def user_roles(request):
    user = request.user
    is_librarian = False
    is_user = False
    if user.is_authenticated:
        is_librarian = user.groups.filter(name="Librarians").exists()
        is_user = user.groups.filter(
            name="library members"
        ).exists()  # or any group you want
    return {
        "is_librarian": is_librarian,
        "is_user": is_user,
    }
