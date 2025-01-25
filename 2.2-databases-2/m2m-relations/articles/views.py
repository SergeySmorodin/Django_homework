from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    # Сортируем статьи по дате публикации в порядке убывания
    articles = Article.objects.prefetch_related('scopes__tag').order_by('-published_at').all()
    context = {
        'object_list': articles,
    }

    return render(request, template, context)
