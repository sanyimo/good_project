from django import forms
from recipes.models import Comment, CuisineType, Recipe, RecipeIngredient, Tag
from parler.forms import TranslatableModelForm
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.forms.widgets import ClearableFileInput
from recipes.models import Category, Ingredient, Allergen, MealType, CookingMethod, Recipe


class RecipeIngredientForm(forms.ModelForm):
    ingredient_name = forms.CharField(
        label=_("Ingrediente")
    )

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient_name', 'quantity', 'unit']
        widgets = {
            'unit': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rellenar ingredient_name si ya hay instancia (para edición)
        if self.instance and self.instance.pk and self.instance.ingredient:
            self.fields['ingredient_name'].initial = self.instance.ingredient.safe_translation_getter('name', any_language=True)
        
        # Añadir aria-labelledby para accesibilidad
        self.fields['ingredient_name'].widget.attrs.update({'aria-labelledby': 'th-ingredient_name'})
        self.fields['quantity'].widget.attrs.update({'aria-labelledby': 'th-quantity'})
        self.fields['unit'].widget.attrs.update({'aria-labelledby': 'th-unit'})

    def clean_ingredient_name(self):
        name = self.cleaned_data.get("ingredient_name")
        if not name or name.strip() == "":
            raise ValidationError(_("Debes escribir el nombre del ingrediente."))
        return name

# # El formset para los ingredientes
def get_recipe_ingredient_formset(extra=0):
    return inlineformset_factory(
        Recipe,
        RecipeIngredient,
        form=RecipeIngredientForm,
        extra=extra,
        can_delete=True
    )


class RecipeForm(TranslatableModelForm):
    photo = forms.ImageField(
        required=False,
        label=_("Foto"),
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Recipe
        fields =  [
            'title',
            'photo',
            'tags',
            'themes',
            'difficulty',
            'prep_time',
            'cook_time',
            'servings',
            'category',
            'cuisine_type',
            'meal_types',
            'allergens',
            'cooking_methods',
            'description',
            'instructions',
            'tips',
        ]

        widgets = {
            'themes': forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
            'tags': forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
            'description': forms.Textarea(attrs={'class': 'hidden', 'id': 'id_description'}),
            'instructions': forms.Textarea(attrs={'class': 'hidden', 'id': 'id_instructions'}),
            'tips': forms.Textarea(attrs={'class': 'hidden', 'id': 'id_tips'}),
            'cooking_methods': forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
            'allergens': forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
            'difficulty': forms.Select(),
        }

        labels = {
            'title': _('Título'),
            'photo': _('Foto'),
            'tags': _('Etiquetas'),
            'themes': _('Temas'),
            'difficulty': _('Dificultad'),
            'prep_time': _('Tiempo de preparación'),
            'cook_time': _('Tiempo de cocción'),
            'servings': _('Porciones'),
            'category': _('Categoría'),
            'cuisine_type': _('Tipo de cocina'),
            'meal_types': _('Tipos de comida'),
            'allergens': _('Alérgenos'),
            'cooking_methods': _('Métodos de cocina'),
            'description': _('Descripción'),
            'instructions': _('Instrucciones'),
            'tips': _('Consejos'),
        }

        help_texts = {
            'instructions': _('Use imágenes con ancho mínimo de 300px y máximo 800px para mejor calidad.'),        
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        image_widget = self.fields['photo'].widget
        if isinstance(image_widget, ClearableFileInput):
            image_widget.initial_text = _("Actualmente")
            image_widget.input_text = _("Puedes subir una nueva para cambiarla. Mínimo 600px")
        
        try:
            has_slug = bool(self.instance.safe_translation_getter('slug', None))
        except (Recipe.DoesNotExist, AttributeError):
            has_slug = False
        
        if has_slug:
            self.fields['photo'].required = False
        else:
            self.fields['photo'].required = True

    def clean_prep_time(self):
        prep_time = self.cleaned_data.get('prep_time')
        errors = []
        if prep_time is None:
            errors.append(_("Debe ingresar el tiempo de preparación."))
        elif prep_time <= 0:
            errors.append(_("El tiempo de preparación debe ser mayor que cero."))
        if errors:
            raise ValidationError(errors)
        return prep_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if servings is not None and servings <= 0:
            raise ValidationError(_("El número de porciones debe ser mayor que cero."))
        return servings

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            w, h = get_image_dimensions(photo)
            if w < 600 or h < 400:
                raise ValidationError(_("La imagen debe tener al menos 600x400 píxeles."))
        return photo
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _('Escribe tu comentario (mín. 10, máx. 300)...'),
                'minlength': 10,
                'maxlength': 300,
                'required': True
            }),
        }
        labels = {
            'content': _('Comentario'),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.recipe = kwargs.pop('recipe', None)
        self.parent = kwargs.pop('parent', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.recipe:
            count = Comment.objects.filter(user=self.user, recipe=self.recipe).count()
            if count >= 5:
                raise ValidationError(_("Has alcanzado el máximo de comentarios para esta receta."))
        return cleaned_data


class SearchForm(forms.Form):
    q = forms.CharField(
        label=_('Buscar por palabra clave'), 
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Ej: pizza, arroz, ensalada...'),
            'aria-label': _('Buscar recetas'),
            'class': 'form-control',
        })
    )
    
    search_in_title = forms.BooleanField(label=_('Título'), required=False, initial=True)
    search_in_description = forms.BooleanField(label=_('Descripción'), required=False)
    search_in_ingredients = forms.BooleanField(label=_('Ingredientes'), required=False)
    search_in_category = forms.BooleanField(label=_('Categoría'), required=False)
    
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        label=_('Ingredientes'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        error_messages={
            'invalid_list': _('Selecciona ingredientes válidos.'),
            'invalid_choice': _('Uno o más ingredientes no son válidos.')
        }
    )
    
    allergens = forms.ModelMultipleChoiceField(
        queryset=Allergen.objects.all(),
        label=_('Excluir alérgenos'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        error_messages={
            'invalid_list': _('Selecciona alérgenos válidos.'),
            'invalid_choice': _('Uno o más alérgenos no son válidos.')
        }
    )
    
    cuisine_type = forms.ModelMultipleChoiceField(
        queryset=CuisineType.objects.all(),
        label=_('Tipo de cocina'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        error_messages={
            'invalid_choice': _('Selecciona un tipo de cocina válido.')
        }
    )
    
    meal_types = forms.ModelMultipleChoiceField(
        queryset=MealType.objects.all(),
        label=_('Tipo de comida'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        error_messages={
            'invalid_list': _('Selecciona tipos de comida válidos.')
        }
    )
    
    difficulty = forms.ChoiceField(
        label=_('Dificultad'),
        choices=[('', _('Todas'))] + list(Recipe._meta.get_field('difficulty').choices), #type: ignore
        required=False,
        widget=forms.Select(attrs={'class': 'select2'}),
        error_messages={
            'invalid_choice': _('Selecciona una dificultad válida.')
        }
    )
    
    cooking_methods = forms.ModelMultipleChoiceField(
        queryset=CookingMethod.objects.all(),
        label=_('Método de preparación'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        error_messages={
            'invalid_list': _('Selecciona método de preparación válido.')
        }
    )
    
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label=_('Categoría'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        error_messages={
            'invalid_choice': _('Selecciona una categoría válida.')
        }
    )
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label=_('Etiquetas'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        error_messages={
            'invalid_choice': _('Selecciona etiqueta válida.')
        }
    )
    
    prep_time_min = forms.IntegerField(
        label=_('Tiempo mínimo (min)'),
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": 'min'}),
        error_messages={
            'invalid': _('Introduce un número válido para el tiempo mínimo.')
        }
    )
    prep_time_max = forms.IntegerField(
        label=_('Tiempo máximo (min)'), 
        required=False,
        widget=forms.NumberInput(attrs={"placeholder": 'max'}),
        error_messages={
            'invalid': _('Introduce un número válido para el tiempo máximo.')
        }
    )
    
    def clean(self):
        cleaned_data = super().clean()
        min_time = cleaned_data.get("prep_time_min")
        max_time = cleaned_data.get("prep_time_max")

        if min_time is not None and max_time is not None and min_time > max_time:
            self.add_error("prep_time_max", _('El tiempo máximo debe ser mayor que el mínimo.'))

        return cleaned_data