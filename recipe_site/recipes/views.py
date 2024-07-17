from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from recipes.models import Category, Recipe, RecipeCategory
from .forms import RecipeForm, SignUpForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, 'Этот email уже используется.')
            else:
                user = form.save()
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Ошибка при регистрации. Пожалуйста, проверьте введенные данные.')
    else:
        form = SignUpForm()
        initial_email = request.session.get('email', '')
        form.fields['email'].initial = initial_email
    return render(request, 'recipes/signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Проверка пользователя по email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не зарегистрирован.')
            return render(request, 'recipes/welcome.html')

        # Аутентификация пользователя
        user = authenticate(username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неправильный email или пароль. Пожалуйста, попробуйте снова или зарегистрируйтесь.')
    return render(request, 'recipes/welcome.html')

def welcome(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        action = request.POST.get('action')

        if action == 'register':
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Этот email уже зарегистрирован.')
                return render(request, 'recipes/welcome.html')
            else:
                request.session['email'] = email
                return redirect('register')
        elif action == 'login':
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Неверный пароль.')
                else:
                    messages.error(request, 'Пользователь с таким email не зарегистрирован.')
    return render(request, 'recipes/welcome.html')



def base(request):
    return render(request, "recipes/base.html")

def index(request):
        random_recipes = Recipe.objects.order_by('?')[:6]  # Получить 5 случайных рецептов
        return render(request, 'recipes/index.html', {'recipes': random_recipes})

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, 'Этот email уже используется.')
            else:
                user = form.save()
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Ошибка при регистрации. Пожалуйста, проверьте введенные данные.')
    else:
        form = SignUpForm()
        initial_email = request.session.get('email', '')
        form.fields['email'].initial = initial_email
    return render(request, 'recipes/signup.html', {'form': form})


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            RecipeCategory.objects.create(recipe=recipe, category=form.cleaned_data['category'])
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})


def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            RecipeCategory.objects.filter(recipe=recipe).delete()
            RecipeCategory.objects.create(recipe=recipe, category=form.cleaned_data['category'])
            return redirect('recipe_detail', id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form})


def recipes_by_category(request):
    categories = Category.objects.all()
    return render(request, 'recipes/recipes_by_category.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipe_categories = RecipeCategory.objects.filter(category=category)
    return render(request, 'recipes/category_detail.html', {'category': category, 'recipe_categories': recipe_categories})
