
from work.bean import Role
from work.bean import Role_Authority

from django.shortcuts import HttpResponse
from django.core import serializers
import json
import hashlib
import jwt
from work.utils.Pagination import Custom_Paginator
from work.utils.ResponseJson import ResponseJsonData

from django.http import JsonResponse




def createRole(request):
 # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    # 获取请求中传递的字段及其值，过滤掉不在Role中的字段
    role_model_fields = [f.name for f in Role.RoleBean._meta.get_fields()]
    insert_fields = {key: value for key, value in python_obj.items() if key in role_model_fields and value is not None}
    Role.RoleBean.objects.create(**insert_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()

def updateRoleById(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    id = request.GET.get("id")
    # 获取请求中传递的字段及其值，过滤掉不在用户表中的字段
    role_model_fields = [f.name for f in Role.RoleBean._meta.get_fields()]
    update_fields = {key: value for key, value in python_obj.items() if key in role_model_fields and value is not None}
    # 更新用户信息，仅更新传递的字段
    Role.RoleBean.objects.filter(id=id).update(**update_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()


def removeRoleById(request):

    res = Role.RoleBean.objects.filter(id=request.GET.get("id")).delete()
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=res)
    return response_data.to_json_response()


def getRole(request):
    page = request.GET.get("pg", 1)
    limit = request.GET.get("limit", 10)
    data_dict = {}

    queryset = Role.RoleBean.objects.filter(**data_dict).order_by("-id")
    # 分页
    data_list = []
    data = Custom_Paginator(queryset, page, limit)
    # 序列化
    for item in data['objects_list']:
        data_list.append({
            'id':item.id,
            'role_name': item.role_name,
            'status': item.status,
            'remark': item.remark,
        })

    # 替换序列化好的数据
    del data['objects_list']
    data['data'] = data_list
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=data)
    return response_data.to_json_response()


def getRoleById(request):
    # 从请求参数中获取 id
    id = request.GET.get("id")
    item =Role.RoleBean.objects.filter(id=id).first()
    if not item:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 item
    result = {
        'role_name': item.role_name,
        'status': item.status,
        'remark': item.remark,
    }
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=result)
    return response_data.to_json_response()



def getRoleAuthoritymission(request):
    roleId = request.GET.get("roleId")
    data_dict = {}
    data_dict["roleId"] = roleId
    queryset = Role_Authority.Role_AuthorityBean.objects.filter(**data_dict).order_by("-id")
    # 分页
    data_list = []
    data = Custom_Paginator(queryset, 1, 999)
    # 序列化
    for item in data['objects_list']:
        data_list.append({
            'id': item.id,
            'roleId': item.roleId,
            'perId': item.perId
        })

    # 替换序列化好的数据
    del data['objects_list']
    data['data'] = data_list
    return ResponseJsonData(errcode=0, errmsg='success', retobj=data_list).to_json_response()

def insertRoleAuthoritymission(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    roleId = python_obj.get("roleId", "");
    perId = python_obj.get("perId", "");
    Role_Authority.Role_AuthorityBean.objects.create(roleId=roleId, perId=perId)
    return ResponseJsonData(errcode=0, errmsg='success', retobj=1).to_json_response()


def deleteRoleAuthoritymission(request):
    res = Role_Authority.Role_AuthorityBean.objects.filter(roleId=request.GET.get("roleId")).delete()
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=res)
    return response_data.to_json_response()