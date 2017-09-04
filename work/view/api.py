from django.shortcuts import HttpResponse, render, redirect
from work.view.account import auth
from work import models
import json


@auth
def api(request):
    """http://127.0.0.1:8080/api?page=1&limit=50  数据接口
    api?type_data=project_data
    api?type_data=domain_data
    """
    type_data = request.GET.get('type_data')
    page = int(request.GET.get('page'))
    limit = int(request.GET.get('limit'))
    data_all = []
    username = request.session.get('username')
    if type_data == 'project_data':
        all_project = models.Domain_info.objects.filter(author=username).values_list('id',
                                                                                     'domain',
                                                                                     'online_date',
                                                                                     'https',
                                                                                     'state',
                                                                                     'product__name',
                                                                                     'project_name',
                                                                                     'apply_date')

        try:
            j = 0
            for i in all_project:
                j += 1
                b = {'id': j,
                     'domain': i[1],
                     'online_date': str(i[2]),
                     'https': i[3],
                     'state': i[4],
                     'product': i[5],
                     'project_name': i[6],
                     'apply_date': i[7]}
                data_all.append(b)
            data = tuple(data_all[i:i + limit] for i in range(0, len(data_all), limit))
            res = {"code": 0, "msg": "", "count": len(data_all), "data": data[page - 1]}
            return HttpResponse(json.dumps(res))
        except IndexError as e:
            return e
    elif type_data == 'domain_data':
        all_project = models.Op_domain.objects.filter(author=username).values_list('id',
                                                                                   'domain',
                                                                                   'IP',
                                                                                   'internal',
                                                                                   'online_date',
                                                                                   'state',
                                                                                   'product__name',
                                                                                   'ops__username',
                                                                                   'status',
                                                                                   'apply_date')
        try:
            j = 0
            for i in all_project:
                j += 1
                b = {'id': j,
                     'domain': i[1],
                     'IP': i[2],
                     'internal': i[3],
                     'online_date': str(i[4]),
                     'state': i[5],
                     'product': i[6],
                     'ops': i[7],
                     'status': i[8],
                     'apply_date': i[9]}
                data_all.append(b)
            data = tuple(data_all[i:i + limit] for i in range(0, len(data_all), limit))
            res = {"code": 0, "msg": "", "count": len(data_all), "data": data[page - 1]}
            # print(res)
            return HttpResponse(json.dumps(res))
        except IndexError as e:
            return e