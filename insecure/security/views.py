from django.http import HttpResponse
from django.shortcuts import render
from security.models import User
from security.forms import SearchForm


# http://127.0.0.1:8000/security/safe/users/1
def safe_users(request, user_id):
    """Uses parameterised query so it's fine"""

    users = User.objects.raw('SELECT * FROM security_user WHERE id = %s', (user_id,))

    return HttpResponse(users)


def admin_index(request):
    """Protected admin page. Requires user to be logged in and staff."""

    if request.user.is_authenticated and request.user.is_staff:
        return HttpResponse('Hello Admin')

    return HttpResponse('No access')


def search(request):
    """Search functionality with XSS protection and input validation."""

    form = SearchForm(request.GET)
    query = ''
    if form.is_valid():
        query = form.cleaned_data['query']

    context = {'query': query}
    return render(request, 'security/search.html', context)