from django.shortcuts import render , get_object_or_404
from .models import Post, Comment
from .forms import NewComment
#creating views

def home(request) :
    context ={ 
    'title': 'الصفحة الرئيسية',
    'posts' : Post.objects.all(),

    }
    #blog/index.html refers to the file at the temblates folder 
    return render(request, 'blog/index.html', context)

def about(request) :
    return render(request, 'blog/about.html', context={'title':'من أنا'})

def post_detail (request, post_id):
    post=  get_object_or_404(Post,pk=post_id)
    comments = post.comments.filter(active=True)
    #التأكد من صحة البيانات قبل الحفظ
    if request.method == 'POST':
        comment_form = NewComment(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = NewComment ()
    else:
        comment_form = NewComment()

    context={
    'title': post,
    'post': post,
    'comments' : comments,
    'comment_form': comment_form,
    }

    return render(request, 'blog/detail.html', context)
