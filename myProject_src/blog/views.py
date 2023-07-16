from django.shortcuts import render
#creating views

def home(request) :
    #blog/index.html refers to the file at the temblates folder 
    return render(request, 'blog/index.html',context={'title': 'Home'})