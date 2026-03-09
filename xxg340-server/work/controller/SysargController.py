
from work.bean import Sysarg
from django.shortcuts import HttpResponse
from django.core import serializers
import json
from work.utils.Pagination import  Custom_Paginator
from django.http import JsonResponse
from work.utils.ResponseJson import ResponseJsonData   
from datetime import datetime



def createSysarg(request):
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    if 'id' in python_obj:
        del python_obj['id']

    # 获取请求中传递的字段及其值，过滤掉不在Sysarg中的字段
    model_fields = [f.name for f in Sysarg.SysargBean._meta.get_fields()]
    fill_fields = {key: value for key, value in python_obj.items() if key in model_fields and value is not None}
    
    fill_fields = {
        (key + '_id') if key in [] else key: value
        for key, value in fill_fields.items()
    }

    
    fill_fields['cd'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        
    
    

    

    Sysarg.SysargBean.objects.create(**fill_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()



def removeSysargById(request):

    Sysarg.SysargBean.objects.filter(id=request.GET.get("id")).delete()
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=1)
    return response_data.to_json_response()


def updateSysargById(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    id = request.GET.get("id")
    # 获取请求中传递的字段及其值，过滤掉不在Sysarg中的字段
    model_fields = [f.name for f in Sysarg.SysargBean._meta.get_fields()]
    fill_fields = {key: value for key, value in python_obj.items() if key in model_fields and value is not None}
    
    fill_fields = {
        (key + '_id') if key in [] else key: value
        for key, value in fill_fields.items()
    }

    
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        

    # 更新Sysarg信息，仅更新传递的字段
    Sysarg.SysargBean.objects.filter(id=id).update(**fill_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()


def getSysarg(request):
    
   
    page = int(request.GET.get("pg", 1))
    limit = int(request.GET.get("limit", 10))
    

    data_dict = {}
    confkey = request.GET.get("confkey","")
    confname = request.GET.get("confname","")
    confvalue = request.GET.get("confvalue","")
    conftype = request.GET.get("conftype","")
    confdesc = request.GET.get("confdesc","")
    cd = request.GET.get("cd","")
    md = request.GET.get("md","")
    
    if confkey:
        data_dict["confkey__contains"] = confkey
    if confname:
        data_dict["confname__contains"] = confname
    if conftype:
        data_dict["conftype"] = conftype
    if confdesc:
        data_dict["confdesc__contains"] = confdesc
    if cd:
        data_dict["cd_gte"] = cd
    if md:
        data_dict["md_gte"] = md
    queryset = Sysarg.SysargBean.objects.filter(**data_dict).order_by("-id")
    
  
    # 获取总数据量
    total_count = queryset.count()

    # 判断limit是否合理
    if limit > total_count:  # 如果limit超过总数据量，返回所有数据
        limit = total_count
    if limit <= 0 or page <= 0:  # 无效的页码或限制
        limit = 1
        page = 1


    # 使用自定义分页器
    data_list = []
    data = Custom_Paginator(queryset, page, limit)

    # 序列化
    for item in data['objects_list']:
        
        data_list.append({
            'id': item.id,
            'confkey': item.confkey,
            'confname': item.confname,
            'confvalue': item.confvalue,
            'conftype': item.conftype,
            'confdesc': item.confdesc,
            'cd': item.cd,
            'md': item.md,
        })

    # 替换序列化好的数据
    del data['objects_list']
    data['data'] = data_list
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=data)
    return response_data.to_json_response()
    


def getSysargById(request):

    # 从请求参数中获取 id
    
    data_dict = {}
    confkey = request.GET.get("confkey","")
    confname = request.GET.get("confname","")
    confvalue = request.GET.get("confvalue","")
    conftype = request.GET.get("conftype","")
    confdesc = request.GET.get("confdesc","")
    cd = request.GET.get("cd","")
    md = request.GET.get("md","")
    
    id = request.GET.get("id")
    if id:
        data_dict["id"] = id
    
    if confkey:
        data_dict["confkey__contains"] = confkey
    if confname:
        data_dict["confname__contains"] = confname
    if conftype:
        data_dict["conftype"] = conftype
    if confdesc:
        data_dict["confdesc__contains"] = confdesc
    if cd:
        data_dict["cd_gte"] = cd
    if md:
        data_dict["md_gte"] = md
    queryset = Sysarg.SysargBean.objects.filter(**data_dict).order_by("-id")
    item =Sysarg.SysargBean.objects.filter(**data_dict).first()
    if not item:
        return ResponseJsonData(errcode=500, errmsg='没有数据', retobj='业务错误')
    # 从数据库中获取到一个对象 item
    
    result = {
        'id': item.id,
            'confkey': item.confkey,
            'confname': item.confname,
            'confvalue': item.confvalue,
            'conftype': item.conftype,
            'confdesc': item.confdesc,
            'cd': item.cd,
            'md': item.md,
    }
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=result)
    return response_data.to_json_response()

