from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, ListView
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from Blog.models import Article

from .forms import ArticleForm
# Create your views here.
def index(request):
    letest_posts = Article.objects.order_by('-timestamp')[:4]
    context = {'letest_posts':letest_posts, 'winners':Article.get_winners()}
    return render(request, 'Blog/BlogHome.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    '''
        create new blogs 
        LoginRequiredMixin : User must be logged in to access this view
    '''
    model = Article
    form_class = ArticleForm
    template_name = 'Blog/add_new_post.html'


    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user  # to add author to article
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Article
    template_name = 'Blog/BlogDetail.html'
    context_object_name = "post"

class PostListView(ListView):
    model = Article
    template_name = "Blog/BlogListing.html"
    context_object_name = "posts"
    paginate_by = 1

def get_paginated_posts(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 1)
    try:
        page_num = request.GET.get("page")
    except:
        page_num = 0
    page_obj = paginator.get_page(page_num)
    
    res = render_to_string("Blog/paginated_posts.html", {'posts':page_obj, 'page_obj':page_obj})
    return JsonResponse({'res':res, 'page_num':page_num, 'total_pages': paginator.num_pages})

def search_blogs(request, q):
    query_articles = Article.objects.filter(title__icontains=q)
    if query_articles.count() > 9:
        posts = query_articles[:9]
    else:
        posts = query_articles
    res = render_to_string("Blog/paginated_posts.html", {'posts':posts})

    result = [[article.title, article.id] for article in query_articles]
    if result:
        return JsonResponse({'status':'success', 'data':result, 'res':res})
    return JsonResponse({'status':'fail'})