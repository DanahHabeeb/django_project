from django import forms
from .models import Comment, Post

class NewComment(forms.ModelForm) :
    class Meta:
        model = Comment
        fields = ('name','email','body')
        
#add one mode field to take the compliance file from user
class PostCreateForm(forms.ModelForm) :
    title = forms.CharField(label='عنوان التقرير', max_length=50)
    content = forms.CharField(label=' وصف التقرير ', widget=forms.Textarea )
    class Meta:
        model = Post
        fields = ['title','content']
        