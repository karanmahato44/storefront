from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request):
    nums = range(1, 11)
    return render(request, 'playground/base.html', context={'nums': nums})
