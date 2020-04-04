"""views.py"""
from django.shortcuts import render

def index(request):
    """いわばhtmlのページ単位の構成物です"""
    # htmlとして返却します
    return render(request, 'shopping/index.html')
