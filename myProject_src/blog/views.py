from typing import Optional
from django.shortcuts import render , get_object_or_404
from .models import Post, Comment
from .forms import NewComment, PostCreateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django .contrib import messages
from django.http import JsonResponse
#creating views

def Try(request) :
    return render(request, 'blog/Try.html', context={'title':'Try'})

def MainPage(request) :
    return render(request, 'blog/TrMainPagey.html', context={'title':'MainPage'})

def home(request) :
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context ={ 
    'title': 'الصفحة الرئيسية',
    'posts' : posts,
    'page' : page,
    }
    #blog/index.html refers to the file at the temblates folder 
    return render(request, 'blog/index.html', context)

def about(request) :
    return render(request, 'blog/about.html', context={'title':'من أنا'})

def post_detail (request, post_id):
    post=  get_object_or_404(Post,pk=post_id)
    comments = post.comments.filter(active=True) #show the comment if it is activated
    #التأكد من صحة البيانات قبل الحفظ
    if request.method == 'POST':
        comment_form = NewComment(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = NewComment () #empty the form
    else:
        comment_form = NewComment()

    context={
    'title': post,
    'post': post,
    'comments' : comments,
    'comment_form': comment_form,
    }

    return render(request, 'blog/detail.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post 
    template_name = 'blog/new_post.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        uploaded_report = self.request.FILES.get('uploaded_report', None)
        if uploaded_report:
            # Check if the file is an Excel file
            if uploaded_report.name.endswith('.xlsx') or uploaded_report.name.endswith('.xls'):
                if uploaded_report.size > 0:
                    form.instance.author = self.request.user
                    return super().form_valid(form)
                else:
                    # File is empty, display warning message
                    messages.warning(self.request, 'الملف المرفق فارغ!')
                    return super().form_invalid(form)
            else:
                # File is not an Excel file, display warning message
                messages.warning(self.request, 'يرجى إرفاق ملف Excel فقط!')
                return super().form_invalid(form)
        else:
            # File not uploaded, display warning message
            messages.warning(self.request, 'يرجى إرفاق تقرير الالتزام قبل التأكيد!')
            return super().form_invalid(form)

        

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):
    model = Post 
    template_name = 'blog/post_update.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
       post = self.get_object()
       if self.request.user == post.author:
           return True
       else:
           return False
       
class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False