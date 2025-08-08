from django import forms
from .models import User

class UserSearchForm(forms.Form):
    user_id = forms.IntegerField(min_value=1)
    
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    
    def clean_query(self):
        query = self.cleaned_data['query']
        # Add additional validation/sanitization if needed
        return query
