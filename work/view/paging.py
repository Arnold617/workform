from django.shortcuts import render,redirect,HttpResponse
from utils import pagination
from work.views import auth
from work import models


# 分页
@auth
def test(request):
    username = request.session.get('username')
    obj = models.User_Info.objects.filter(username=username).all()
    LIST = []
    for project in obj:
        for item in project.domain_info_set.all():
            LIST.append(item)
    #     for j2 in i.op_domain_set.all():
    #         print(j2.domain, j2.online_date, j2.product.name,j2.status)
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.GET.get('per_page_count', 10)
    val = int(val)
    print(type(val), val)
    page_obj = pagination.Page(current_page, len(LIST), val)
    data = LIST[page_obj.start:page_obj.end]

    page_str = page_obj.page_str('/test.html')
    return render(request, 'test.html', {'data': data, 'page_str': page_str})

