
from django.contrib import admin

from recipes.models import Category, Recipe, RecipeCategory, Profile
admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(RecipeCategory)
admin.site.register(Profile)
