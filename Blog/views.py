from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView

from Blog.models import Article

from .forms import ArticleForm
# Create your views here.
def index(request):
    return render(request, 'Blog/home.html')

def add_new_post(request):
    if request.POST:
        form = ArticleForm(request.POST)
        if form.is_valid():
            f = form.save()
            return HttpResponse(f.content)
        print(form.errors)
    form = ArticleForm()
    return render(request,'Blog/add_article.html', {'form':form})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'Blog/add_article.html'


    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user  # to add author to article
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Article
    template_name = 'Blog/blog_detail copy.html'