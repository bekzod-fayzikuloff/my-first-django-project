from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count





def post_list(request, tag_slug =None):
    '''Функция которая, является неким обрабочкиком которая группирует "страницы" нашего
    блога показывая по 3статьи на страницу для этого есть встроенный класс постраничного отображения
    т.е пакет django.core.paginator и его классы-пагинаторы'''
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5)  # По 4 статьи на каждой странице.
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    is_paginated = posts.has_other_pages()

    if posts.has_previous():
        prev_url = '?page={}'.format(posts.previous_page_number())
    else:
        prev_url = ''

    if posts.has_next():
        next_url = '?page={}'.format(posts.next_page_number())
    else:
        next_url = ''

    context = {
        'page': page,
        'posts': posts,
        'is_paginated': is_paginated,
        'tag': tag,
        'prev_url': prev_url,
        'next_url': next_url
    }

    return render(request, 'blog/post/list.html', context=context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    comments_form = None

    if request.method == 'POST':
        comments_form = CommentForm(data=request.POST)

        if comments_form.is_valid():
            new_comment = comments_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

        else:
            comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                          .exclude(id = post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags'))\
                                           .order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                    'comments': comments,
                                                    'new_comment': new_comment,
                                                    'comment_form': comments_form,
                                                    'similar_posts': similar_posts},
                  )


def main_page(request):
    return render(request, 'blog/post/index.html')


def about(request):
    return render(request, 'blog/post/about.html')


def contact(request):
    return render(request, 'blog/post/contact.html')

