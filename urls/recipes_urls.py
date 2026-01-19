from django.urls import path
from django.utils.translation import gettext_lazy as _
from views.recipes_views import (
    CategoryDetailView,
    RecipeListView,
    recipe_detail, 
    random_recipe_json,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    rate_recipe,
    add_comment,
    toggle_favorite,
)

app_name = 'recipes'
category_prefix = _('categories/')

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path(_('new-recipe/'), RecipeCreateView.as_view(), name='recipe_create'),
    path('random-json/', random_recipe_json, name='random_recipe_json'),
    path(_("toggle-favorite/"), toggle_favorite, name="toggle_favorite"),
    path('<slug:slug>/', recipe_detail, name='recipe_detail'),
    path(_('<slug:slug>/update/'), RecipeUpdateView.as_view(), name='recipe_update'),
    path(_('<slug:slug>/delete/'), RecipeDeleteView.as_view(), name='recipe_delete'),
    path(_('<slug:slug>/rate/'), rate_recipe, name='rate_recipe'),
    path(_('<slug:slug>/comment/'), add_comment, name='add_comment'),
    path(category_prefix  + '<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]