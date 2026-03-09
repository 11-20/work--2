
from work.bean import User

from django.shortcuts import HttpResponse
from django.core import serializers
import json
import hashlib
import jwt
from work.utils.Pagination import Custom_Paginator
from work.utils.ResponseJson import ResponseJsonData

from work.bean import Role
from work.bean import Role_Authority
from work.bean import Authority
from work.utils.Utils import Utils

from django.core.files.storage import FileSystemStorage





def getWebsiteInfo(request):
    currentUser = request.user
    # 获取该用户权限数据
    roleId = currentUser["role_id"]
    data_dict = {}
    data_dict["roleId"] = roleId
    queryset = Role_Authority.Role_AuthorityBean.objects.filter(**data_dict).order_by("-id")
    # 用户的权限id
    perIds = []
    data = Custom_Paginator(queryset, 1, 999)
    # 序列化
    for item in data['objects_list']:
        perIds.append(item.perId)

    del data['objects_list']
    # 获取该用户权限数据 end

    # 获取所有权限数据
    allAuthoritymissions = []
    pdata = Custom_Paginator(Authority.AuthorityBean.objects.order_by("-id"), 1, 999)
    # 序列化
    for item in pdata['objects_list']:
        allAuthoritymissions.append({
            'id': item.id,
            'parentId': item.parentId,
            'perName': item.perName,
            'path': item.path,
            'perUrl': item.perUrl,
            'perIcon': item.perIcon,
            'name': item.perName,
            'url': item.perUrl
        })
    # 替换序列化好的数据
    del pdata['objects_list']
    filterAuthoritymissions = []
    if currentUser.get('is_super') == 1:
        # 超级管理员返回所有权限
        print("超级管理员返回所有权限========================================")
        filterAuthoritymissions = allAuthoritymissions
    else:
        print("非超级管理员查询权限")
        filterAuthoritymissions = [
            {
                'id': item['id'],
                'parentId': item['parentId'],
                'perName': item['perName'],
                'path': item['path'],
                'perUrl': item['perUrl'],
                'perIcon': item['perIcon'],
                'name': item['perName'],
                'url': item['url']
            }
            for item in allAuthoritymissions
            if str(item['id']) in perIds or item['id'] == 3
        ]
    filteredAuthoritymissionsData = Utils.convert_to_tree(filterAuthoritymissions)[0]['children']
    websiteData = {
        "menu": filteredAuthoritymissionsData,
        "currentUser": currentUser,
        "siteConfig": {}
    };

    return ResponseJsonData(errcode=0, errmsg='success', retobj=websiteData).to_json_response()


def uploadSingleFile(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # 使用FileSystemStorage保存文件到MEDIA_ROOT目录
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        # 构建文件的访问URL
        file_url = "http://127.0.0.1:8080"+ fs.url(filename)

        # 返回包含文件访问地址的JSON响应
        return ResponseJsonData(errcode=0, errmsg='success', retobj=file_url).to_json_response()


    return ResponseJsonData(errcode=500, errmsg='文件上传失败', retobj="业务错误").to_json_response()