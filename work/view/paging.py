from django.shortcuts import render,redirect,HttpResponse
from work import models
from django import views
from utils import pagination
from work.views import auth

# 分页

LIST = []
for i in range(103):
    LIST.append(i)

@auth
def mine(request):
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    page_obj = pagination.Page(current_page, len(LIST))
    data = LIST[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/mine.html')
    return render(request, 'mine.html', {'data': data, 'page_str': page_str})
