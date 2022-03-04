from pickle import FALSE
from sqlite3 import Timestamp
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, ListView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
import json

from Blog.models import Article, ArticleComment

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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        try:
            comments = post.articlecomment_set.order_by("timestamp")
            if comments.count() > 10:
                context['comments'] = comments[:10]
                context['next_page_no'] = 2
                context['has_next_page'] = True
            else:
                context['comments'] = comments
                context['next_page_no'] = 0
                context['has_next_page']= FALSE
        except:
            context['comments'] = None
        return context

class PostListView(ListView):
    model = Article
    template_name = "Blog/BlogListing.html"
    context_object_name = "posts"
    paginate_by = 9


# Ajax functions
def get_paginated_posts(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 9)
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


# to add comment
def add_comment(request):
    comment = json.load(request)
    try:
        article = Article.objects.get(id = comment['article_id'])
        comment_ = ArticleComment(
                                            user=request.user,
                                            Article = article,
                                            comment_text = comment['comment_text'],
                                            )
        comment_.save()
        return JsonResponse({'status':'success', 'comment': {'user':comment_.user.name, 'comment_text': comment_.comment_text}})
    except:
        return JsonResponse({'status':'fail'})


# get comments (paginated)
def get_comments(request, article_no):
    try:
        article = Article.objects.get(id = article_no)
        paginator = Paginator(article.articlecomment_set.order_by("timestamp"), 10)
        page_no = 0
        try:
            page_no = request.GET.get("page")
        except Exception as e:
            return JsonResponse({"status":"fail", "msg":"page_not found"})
        page_obj = paginator.get_page(page_no)
        context = {'comments':page_obj, 'has_next_page':page_obj.has_next(), 'post':article}
        if page_obj.has_next():
            context["next_page_no"] = page_obj.next_page_number()
        else:
             context['next_page_no'] = 0
        res = render_to_string("Blog/comment_template.html", context)
        return JsonResponse({'status':'success', 'res':res})
    except Exception as e:
        return JsonResponse({'status':'fail'})
    