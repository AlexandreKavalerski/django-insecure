from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.db import connection
from django.http import JsonResponse
from .forms import UserInputForm

@csrf_protect
def secure_view(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            # Using parameters with the ORM instead of raw SQL
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Example of secure database query using ORM
            from django.contrib.auth.models import User
            users = User.objects.filter(username=name)
            
            # If raw SQL is absolutely necessary, use parameterized queries
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM auth_user WHERE username = %s",
                    [name]
                )
                row = cursor.fetchone()
            
            return JsonResponse({'status': 'success'})
    else:
        form = UserInputForm()
    
    return render(request, 'security/secure_form.html', {'form': form})

# Add more views as needed, always using csrf_protect and proper form validation
