from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#tables translelated into the db
# fields are title , content ...
# db is written using pythonand needed to be transformed to sql using commands 
#1. python manage.py makemigrations from python to sql
#2. python manage.py migrate execute the sqql and create the db
class Post( models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now) #created first time when blog is created
    post_update = models.DateTimeField(auto_now=True) #updated every time the blog is alterd
    author = models.ForeignKey(User, on_delete= models.CASCADE) #user is from jango tables


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-post_date',)

class Comment (models.Model):
    name = models.CharField(max_length=30, verbose_name="الإسم")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    body = models.TextField(verbose_name="التعليق")
    comment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
        return 'علق {} على {}.'.format(self.name, self.post)
    class Meta:
        ordering = ('-comment_date',)