from django import forms

from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'tags',
            'cooking_time',
            'text',
            'image',
            # 'ingredients'
        )
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        data = self.cleaned_data['title']
        if not data:
            raise forms.ValidationError('Добавьте название рецепта')
        return data



    # def clean(self):
    #     ingredient_names = self.data.getlist('nameIngredient')
    #     ingredient_units = self.data.getlist('unitsIngredient')
    #     ingredient_amounts = self.data.getlist('valueIngredient')
    #     ingredients_clean = []
    #     for ingredient in zip(ingredient_names, ingredient_units,
    #                           ingredient_amounts):
    #         if int(ingredient[2]) < 0:
    #             raise forms.ValidationError('Количество ингредиентов должно быть больше нуля')
    #     return ingredients_clean
    # при исключении отрицательных рецептов выходит ошибка 'list' object has no attribute 'get'


            # else:
            #     ingredients_clean.append({
            #         'title': ingredient[0],
            #         'dimension': ingredient[1],
            #         'quantity': ingredient[2]
            #     })
        # if not ingredients_clean:
        #     raise forms.ValidationError('Добавьте ингредиент')
        # return ingredients_clean

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.author = self.initial['author']
    #     instance.save()
    #     ingredients = self.cleaned_data['ingredients']
    #     self.cleaned_data['ingredients'] = []
    #     self.save_m2m()
    #     Ingredient.objects.bulk_create(
    #         get_ingredients_from_form(ingredients, instance))
    #     return instance