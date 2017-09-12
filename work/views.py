# Create your views here.
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import render,redirect,HttpResponse
from work import models
import time
from work.view.account import auth
from utils import pagination


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
        # obj = models.Domain_info.objects.filter(id=1).first()
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
        online_date = str(request.POST.get('date'))
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
                                            online_date=online_date,
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
    if request.method == 'GET':
        obj = models.User_Info.objects.filter(username='feixiang').all()
        return render(request, 'test.html', {'obj': obj})


@auth
def backlog(request):
    if request.method == 'GET':
        username = request.session.get('username')
        obj = models.User_Info.objects.filter(username=username).all()
        LIST = []
        for project in obj:
            for item in project.domain_info_set.all():
                if item.status == '0':
                    LIST.append(item)
            # for item2 in project.op_domain_set.all():
            #     if item2.status == '0':
            #         LIST.append(item2)
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        # val = request.GET.get('per_page_count', 10)
        val = int(20)
        page_obj = pagination.Page(current_page, len(LIST), val)
        data = LIST[page_obj.start:page_obj.end]

        page_str = page_obj.page_str('/backlog.html')
        return render(request, 'backlog.html', {'data': data, 'page_str': page_str})


# @auth
def backlog_detail(request, nid):
    if request.method == 'GET':
        obj = models.Domain_info.objects.filter(id=nid).first()
        return render(request, 'backlog-detail.html', {'obj': obj})
    elif request.method == 'POST':
        # nid = request.POST.get('nid')
        state = request.POST.get('state')
        ops = request.POST.get('ops')
        status = request.POST.get('status')
        print(ops, nid, status)
        if status:
            status = 1
        else:
            status = 0
        if nid:
            models.Domain_info.objects.filter(id=nid).update(ops_id=ops, state=state, status=status)
            return redirect('/mine.html')


@auth
def mine(request):
    return render(request, 'mine.html')


@csrf_exempt
def upload(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    elif request.method =='POST':
        # username = request.POST.get('username')
        fafafa = request.FILES.get('fafafa')
        import os
        img_path = os.path.join('static/images',fafafa.name)
        print(img_path)
        with open(img_path,'wb') as f:
            for item in fafafa.chunks():
                f.write(item)

        ret = {'code': True , 'data': img_path}
        import json
        return HttpResponse(json.dumps(ret))


# 组合搜索
def article(request, *args, **kwargs):
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v == '0':
            pass
        else:
            condition[k] = v
    article_type_list = models.ArticleType.objects.all()
    category_list = models.Category.objects.all()
    result = models.Article.objects.filter(**condition)
    print(kwargs)
    return render(request,'article.html',{'article_type_list': article_type_list,
                                          'category_list': category_list,
                                          'result': result,
                                          'arg_dict': kwargs})