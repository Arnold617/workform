# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from work import models

import time


from work.view.account import auth
# 主页
@auth
def index(request):
    username =request.session.get('username')
    obj = models.Op_domain.objects.all()
    # 从session中获取值
    return render(request,'index.html', {'obj': obj})


# 主模板
# @auth
# def base(request):
#     return render(request, 'base.html')


@auth
def new_project(request):
    if request.method == 'GET':
        obj = models.Domain_info.objects.filter(id=1).first()
        return render(request, 'new_project.html')
    elif request.method == 'POST':
        project_name = request.POST.get('project_name')
        domain = request.POST.get('domain')
        date = request.POST.get('date')
        apply_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        https = request.POST.get('https')
        if https:
            https = "YES"
        else:
            https = "NO"
        state = str(request.POST.get('state'))
        product = request.POST.get('product')
        author = request.session.get('username')
        ops = request.POST.get('ops')
        status = 0
        print(domain, date, https, state, product, ops)
        if domain and product and state:
            models.Domain_info.objects.create(project_name=project_name,
                                              domain=domain,
                                              online_date=date,
                                              apply_date=apply_date,
                                              https=https,
                                              product_id=product,
                                              state=state,
                                              author=author,
                                              ops_id=ops,
                                              status=status)
            return redirect('/index/')
        else:
            return render(request, 'new_project.html')


@auth
def set_domain(request):
    if request.method == 'GET':
        return render(request, 'set_domain.html')
    elif request.method =='POST':
        domain = request.POST.get('domain')
        IP = request.POST.get('IP')
        date = request.POST.get('date')
        apply_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        internal = request.POST.get('internal')
        if  not internal:
            internal = 'NO'
        else:
            internal = 'YES'
        state = request.POST.get('state')
        product = request.POST.get('product')
        author = request.session.get('username')
        ops = request.POST.get('ops')
        status = 0
        # print(domain, IP, date, internal, state, product)
        if domain and product and state:
            models.Op_domain.objects.create(domain=domain,
                                            IP=IP,
                                            online_date=date,
                                            apply_date=apply_date,
                                            internal=internal,
                                            product_id=product,
                                            state=state,
                                            author=author,
                                            ops_id=ops,
                                            status=status)
            return redirect('/index/')
        else:
            return render(request, 'set_domain.html')


def test(request):
    return render(request, 'test.html')

@auth
def mine(request):
    return render(request, 'mine.html')