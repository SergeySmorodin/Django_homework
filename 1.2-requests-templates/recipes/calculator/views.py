from django.shortcuts import render, get_object_or_404
from django.http import Http404

# http://127.0.0.1:8000/omlet/
# http://127.0.0.1:8000/pasta/
# http://127.0.0.1:8000/buter/
# http://127.0.0.1:8000/omlet/?servings=4
# http://127.0.0.1:8000/omlet/?servings=-1
# http://127.0.0.1:8000/salat/

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 300,
        'сыр, г': 50,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def to_cook(request, dish_name):
    template_name = "calculator/index.html"

    if dish_name not in DATA:
        raise Http404("Рецепт не найден")

    recipe = DATA[dish_name]
    servings = int(request.GET.get('servings', 1))

    try:
        if servings < 1:
            raise ValueError
    except ValueError:
        servings = 1

    result = dict((ingredient, amount * servings) for ingredient, amount in recipe.items())

    context = {
        'recipe': result,
    }

    return render(request, template_name, context)












































