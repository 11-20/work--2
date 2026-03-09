
from work.bean import Authority

from django.shortcuts import HttpResponse
from django.core import serializers
import json
import hashlib
import jwt
from work.utils.Pagination import Custom_Paginator
from work.utils.ResponseJson import ResponseJsonData

from django.http import JsonResponse
from work.utils.Utils import Utils



def createAuthority(request):
 # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    # 获取请求中传递的字段及其值，过滤掉不在Authority中的字段
    per_model_fields = [f.name for f in Authority.AuthorityBean._meta.get_fields()]
    insert_fields = {key: value for key, value in python_obj.items() if key in per_model_fields and value is not None}
    Authority.AuthorityBean.objects.create(**insert_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()

def updateAuthorityById(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    id = request.GET.get("id")
    # 获取请求中传递的字段及其值，过滤掉不在用户表中的字段
    per_model_fields = [f.name for f in Authority.AuthorityBean._meta.get_fields()]
    update_fields = {key: value for key, value in python_obj.items() if key in per_model_fields and value is not None}
    # 更新用户信息，仅更新传递的字段
    Authority.AuthorityBean.objects.filter(id=id).update(**update_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()


def removeAuthorityById(request):

    res = Authority.AuthorityBean.objects.filter(id=request.GET.get("id")).delete()
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=res)
    return response_data.to_json_response()


def getAuthority(request):
    page = request.GET.get("pg", 1)
    limit = request.GET.get("limit", 999)
    data_dict = {}
    queryset = Authority.AuthorityBean.objects.filter(**data_dict).order_by("-id")
    # 分页
    data_list = []
    data = Custom_Paginator(queryset, page, limit)
    # 序列化
    for item in data['objects_list']:
        data_list.append({
            'id':item.id,
            'parentId': item.parentId,
            'perName': item.perName,
            'path': item.path,
            'perUrl': item.perUrl,
            'perIcon': item.perIcon,
        })

    # 替换序列化好的数据
    del data['objects_list']
    perdata = Utils.convert_to_tree(data_list)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=perdata[0]['children'])
    return response_data.to_json_response()


def getAuthorityById(request):
    # 从请求参数中获取 id
    id = request.GET.get("id")
    item =Authority.AuthorityBean.objects.filter(id=id).first()
    if not item:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 item
    result = {
        'parentId': item.parentId,
        'perName': item.perName,
        'path': item.path,
        'perUrl': item.perUrl,
        'perIcon': item.perIcon,
    }
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=result)
    return response_data.to_json_response()
