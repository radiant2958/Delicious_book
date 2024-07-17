from django import views
from django.urls import path
from django.conf.urls.static import static

from recipe_site import settings

from .views import add_recipe, category_detail, custom_login, edit_recipe, recipe_detail, recipes_by_category, register, welcome, signup, base,index

urlpatterns = [
    path('login/', custom_login, name='login'),
    path('register/', register, name='register'),
    path('', welcome, name='welcome'),
    # path('login/', views.custom_login, name='login'),
    path('signup/',signup, name='signup'),
    path('base/',base, name='base'),
    path ("index/",index, name='index' ),
    path('recipe/<int:id>/', recipe_detail, name='recipe_detail'),
    path('recipe/add/', add_recipe, name='add_recipe'),
    path('recipe/edit/<int:id>/', edit_recipe, name='edit_recipe'),
    path('categories/', recipes_by_category, name='recipes_by_category'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])