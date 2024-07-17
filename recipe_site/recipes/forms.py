from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Recipe

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cooking_time', 'image', 'ingredients', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'steps': forms.Textarea(attrs={'rows': 5}),
            'ingredients': forms.Textarea(attrs={'rows': 3}),
        }