
from work.bean import User

from django.shortcuts import HttpResponse
from django.core import serializers
import json
import hashlib
import jwt
from work.utils.Pagination import Custom_Paginator
from work.utils.ResponseJson import ResponseJsonData

from django.http import JsonResponse




def createUser(request):

    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)

    user_name = python_obj.get("user_name","");
    avatar = python_obj.get("avatar","");
    phone = python_obj.get("phone","");
    email = python_obj.get("email","");
    password = python_obj.get("password","");
    sex = python_obj.get("sex","");
    status = python_obj.get("status","");
    remark = python_obj.get("remark","");
    is_super = python_obj.get("is_super","");
    role_id = python_obj.get("role_id","");

    # 如果没有提供密码，则使用手机号后六位作为默认密码
    if not password:
        password = phone[-6:]

    # 使用 hashlib 对密码进行 MD5 加密
    md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()


    User.UserBean.objects.create(
        user_name=user_name,
        avatar=avatar,
        phone=phone,
        email=email,
        password=md5_password,
        sex=sex,
        status=status,
        remark=remark,
        is_super=is_super,
        role_id_id=role_id, # 外键字段需要加一个_id 后缀
    )

    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()



def removeUserById(request):

    res = User.UserBean.objects.filter(id=request.GET.get("id")).delete()
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=res)
    return response_data.to_json_response()


def updateUserById(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    id = request.GET.get("id")
    # 获取请求中传递的字段及其值，过滤掉不在用户表中的字段
    user_model_fields = [f.name for f in User.UserBean._meta.get_fields()]
    update_fields = {key: value for key, value in python_obj.items() if key in user_model_fields and value is not None}
    # 更新用户信息，仅更新传递的字段
    User.UserBean.objects.filter(id=id).update(**update_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()


def reset_password(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    user_id = request.GET.get("id")
    phone = python_obj.get("phone", "")
    # 如果没有提供密码，则使用手机号后六位作为默认密码
    password = phone[-6:]
    # 使用 hashlib 对密码进行 MD5 加密
    md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    # 更新用户密码
    User.UserBean.objects.filter(id=user_id).update(password=md5_password)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()


def getUser(request):
    page = request.GET.get("pg", 1)
    limit = request.GET.get("limit", 10)
    data_dict = {}
    queryset = User.UserBean.objects.filter(**data_dict).order_by("-id")
    # 分页
    data_list = []
    data = Custom_Paginator(queryset, page, limit)
    # 序列化
    for item in data['objects_list']:
        role_id = getattr(item, 'role_id_id', None)

        if role_id:
            try:
                role_name = item.role_id.role_name if item.role_id else ""
            except Exception:  # 捕获所有可能的异常
                role_name = ""
        data_list.append({
            'id': item.id,
            'user_name': item.user_name,
            'avatar': item.avatar,
            'phone': item.phone,
            'email': item.email,
            'password': item.password,
            'sex': item.sex,
            'status': item.status,
            'remark': item.remark,
            'is_super': item.is_super,
            'role_id': role_id,  # 使用处理后的值
            'role_name': role_name,  # 使用处理后的值
        })

    # 替换序列化好的数据
    del data['objects_list']
    data['data'] = data_list
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=data)
    return response_data.to_json_response()

def getUserById(request):
    # 从请求参数中获取 id
    id = request.GET.get("id")
    item =User.UserBean.objects.filter(id=id).first()
    if not item:
        return JsonResponse({"status": False, 'error': "数据不存在。"})


    role_id = getattr(item, 'role_id_id', None)
    if role_id:
        try:

            role_name = item.role_id.role_name if item.role_id else ""
        except Exception:  # 捕获所有可能的异常
            role_name = ""

    # 从数据库中获取到一个对象 item
    result = {
        "id": item.id,
        'user_name': item.user_name,
        'avatar': item.avatar,
        'phone': item.phone,
        'email': item.email,
        'password': item.password,
        'status': item.status,
        'remark': item.remark,
        'is_super': item.is_super,
        'role_id': role_id,
        'role_name': role_name,
        'sex': item.sex,
    }
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=result)
    return response_data.to_json_response()


def register(request):
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)

    user_name = python_obj.get("user_name", "");
    avatar = python_obj.get("avatar", "");
    phone = python_obj.get("phone", "");
    email = python_obj.get("email", "");
    password = python_obj.get("password", "");
    sex = python_obj.get("sex", "");
    status = 1
    role_id = python_obj.get("role_id", "3");
    remark = python_obj.get("remark", "");


    # 如果没有提供密码，则使用手机号后六位作为默认密码
    if not password:
        password = phone[-6:]

    # 使用 hashlib 对密码进行 MD5 加密
    md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()

    User.UserBean.objects.create(
        user_name=user_name,
        avatar=avatar,
        phone=phone,
        email=email,
        password=md5_password,
        sex=sex,
        status=status,
        remark=remark,
        is_super=0,
        role_id_id=role_id,  # 外键字段需要加一个_id 后缀
    )

    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()

def login(request):
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    phone = python_obj.get("phone", "");
    password = python_obj.get("password", "");

    item = User.UserBean.objects.filter(phone=phone).first()
    if not item:
        return ResponseJsonData(errcode=500, errmsg='用户不存在', retobj="业务错误").to_json_response()
    # 使用 hashlib 对密码进行 MD5 加密
    md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    # 判断密码是否相等
    if md5_password == item.password:
        # 密码匹配，生成 JWT 令牌
        payload = {
            'id': item.id,
            'user_id': item.id,
            'user_name': item.user_name,
            'role_id': item.role_id.id,
            'avatar': item.avatar,
            'is_super': item.is_super,
            'email': item.email,
            'phone': item.phone,
        }
        token = jwt.encode(payload, 'jwtSecret', algorithm='HS256')
        # 返回生成的令牌
        return ResponseJsonData(errcode=0, errmsg='登录成功', retobj={'authToken': token}).to_json_response()
    else:
        return ResponseJsonData(errcode=500, errmsg='密码错误', retobj="业务错误").to_json_response()


