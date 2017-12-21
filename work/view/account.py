from django.shortcuts import render, redirect, HttpResponse
from work import models
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from work.forms import FM_REGISTER
from io import BytesIO
from utils.check_code import create_validate_code


def check_code(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


# @csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        auth_code =  request.POST.get('check_code')
        if auth_code.upper() == request.session['CheckCode'].upper():
            if not username:
                return render(request, 'login.html', {'error_msg': "User or password is empty"})
            else:
                try:
                    obj = models.User_Info.objects.filter(username=username).first()
                    if  obj.username == username and obj.password == password:
                        request.session['username'] = username
                        request.session['is_login'] = True
                        if request.POST.get('remember', None) == '1':
                            # 超时时间(秒)
                            request.session.set_expiry(60 * 60 *60)
                        else:
                            request.session.set_expiry(20 * 60)
                        return redirect('/index/')
                    else:
                        return render(request, 'login.html', {'error_msg': "User or password error"})
                except AttributeError as e:
                    return render(request, 'login.html', {'error_msg': "User or password error"})
        else:
            return render(request, 'login.html', {'error_msg': 'auth_code error'} )

def auth(func):
    def inner(request, *args, **kwargs):
        v = request.session.get('is_login',None)
        if not v:
            return redirect('/login/')
        return func(request, *args, **kwargs)
    return inner


def register(request):
    if request.method == 'GET':
        obj = FM_REGISTER()
        return render(request, 'register.html', {'obj': obj})
    elif request.method == 'POST':
        obj = FM_REGISTER(request.POST)
        r1 = obj.is_valid()   # 返回是True 或者 False
        if r1:
            user = request.POST.get('username')
            obj_user = models.User_Info.objects.filter(username=user).first()
            if not obj_user:
                models.User_Info.objects.create(**obj.cleaned_data)
                return redirect('/login/')
            else:
                return render(request, 'register.html', {'obj': obj, 'error_page': 'User already exists'})
        else:
            return render(request, 'register.html', {'obj': obj})


# 注销功能
def logout(request):
    request.session.clear()
    return redirect('/login')


# 找回密码
def forgot(request):
    return render(request, 'forgot.html')