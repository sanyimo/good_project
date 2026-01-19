from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, CookingMethod, Allergen, Ingredient, Recipe, RecipeIngredient, CuisineType
from django.db.models import Count
  

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    autocomplete_fields = ['ingredient']
    verbose_name = "Ingrediente"
    verbose_name_plural = "Ingredientes"
    fields = ['ingredient', 'quantity', 'unit']


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    search_fields = ['translations__name']
    list_display = ['__str__', 'recipe_count']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(num_recipes=Count('recipes'))

    def recipe_count(self, obj):
        return obj.num_recipes
    recipe_count.short_description = 'Recetas'


@admin.register(Ingredient)
class IngredientAdmin(TranslatableAdmin):
    search_fields = ['translations__name']
    

@admin.register(Allergen)
class AllergenAdmin(TranslatableAdmin):
    search_fields = ['translations__name']
    
    
@admin.register(CookingMethod)
class CookingMethodAdmin(TranslatableAdmin):
    list_display = ['__str__']
    

@admin.register(CuisineType)
class CuisineTypeAdmin(TranslatableAdmin):
    search_fields = ['translations__name']

    
@admin.register(Recipe)
class RecipeAdmin(TranslatableAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['title', 'author', 'category', 'difficulty', 'prep_time', 'featured']
    list_filter = ['difficulty', 'category', 'featured', 'meal_types', 'cooking_methods', 'cuisine_type']
    search_fields = ['translations__title']
    list_editable = ('featured',)
    autocomplete_fields = ['ingredients', 'allergens', 'category', 'author']

    def display_meal_types(self, obj):
        return ", ".join([str(mt) for mt in obj.meal_types.all()])
    display_meal_types.short_description = 'Meal Types'