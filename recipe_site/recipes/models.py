from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    steps = models.TextField()
    cooking_time = models.IntegerField(help_text="Время приготовления в минутах")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.TextField(help_text="Перечислите ингредиенты, разделяя их запятой")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
    

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    extra_info = models.CharField(max_length=255, blank=True, null=True)  

    class Meta:
        unique_together = ('recipe', 'category')  

    def __str__(self):
        return f"{self.recipe.title} - {self.category.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_professional = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

