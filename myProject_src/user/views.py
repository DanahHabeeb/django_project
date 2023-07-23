from django.shortcuts import render
from .forms import UserCreationForm

def register(request):
    form = UserCreationForm()
    return render(request, 'user/register.html', {
        'title': 'التسجيل',
        'form': form,
    })

