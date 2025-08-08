import json
import os
import jwt
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.utils.html import escape
from django.core.exceptions import ValidationError

from security.models import User
from security.forms import UserSearchForm, SearchForm


@csrf_protect
@require_http_methods(["GET"])
def get_user(request, user_id):
    """Secure way to get user by ID using Django ORM"""
    form = UserSearchForm({'user_id': user_id})
    
    if not form.is_valid():
        return JsonResponse({'error': 'Invalid user ID'}, status=400)
    
    try:
        user = User.objects.get(id=form.cleaned_data['user_id'])
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            # Add other safe fields as needed
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@csrf_protect
@require_http_methods(["POST"])
def create_user(request):
    """Secure way to create a user"""
    try:
        data = json.loads(request.body)
        user = User.objects.create(**data)
        return JsonResponse({'id': user.id}, status=201)
    except (json.JSONDecodeError, ValidationError) as e:
        return JsonResponse({'error': str(e)}, status=400)


def create_jwt_token(user_id, is_admin=False):
    """Create a secure JWT token"""
    return jwt.encode(
        {
            'user_id': user_id,
            'is_admin': is_admin
        }, 
        settings.SECRET_KEY, 
        algorithm='HS256'
    )

@csrf_protect
@require_http_methods(["GET"])
def admin_index(request):
    """Protected admin page using secure JWT tokens"""
    try:
        token = request.COOKIES.get('auth_token', '')
        if not token:
            return HttpResponseForbidden('No access token provided')
            
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        
        if payload.get('is_admin'):
            return HttpResponse('Hello Admin')
        
        return HttpResponseForbidden('Not authorized')
    except jwt.InvalidTokenError:
        return HttpResponseForbidden('Invalid token')

@csrf_protect
@require_http_methods(["GET"])
def search(request):
    """Secure search functionality with XSS protection"""
    form = SearchForm(request.GET)
    
    if not form.is_valid():
        return JsonResponse({'error': 'Invalid search query'}, status=400)
        
    query = form.cleaned_data['query']
    
    # Always escape user input to prevent XSS
    safe_query = escape(query)
    
    return JsonResponse({
        'query': safe_query,
        'results': []  # Add your actual search logic here
    })

@csrf_protect
@require_http_methods(["GET"])
def log(request):
    """Secure logging endpoint"""
    form = SearchForm(request.GET)
    
    if not form.is_valid():
        return JsonResponse({'error': 'Invalid log data'}, status=400)
        
    # Log safely - avoid printing raw user input
    safe_string = escape(form.cleaned_data['query'])
    print(f"Logged (sanitized): {safe_string}")
    
    return HttpResponse('Logged successfully')
