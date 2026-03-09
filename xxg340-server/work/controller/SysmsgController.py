
from work.bean import Sysmsg
from django.shortcuts import HttpResponse
from django.core import serializers
import json
from work.utils.Pagination import  Custom_Paginator
from django.http import JsonResponse
from work.utils.ResponseJson import ResponseJsonData   
from datetime import datetime



def createSysmsg(request):
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    if 'id' in python_obj:
        del python_obj['id']

    # 获取请求中传递的字段及其值，过滤掉不在Sysmsg中的字段
    model_fields = [f.name for f in Sysmsg.SysmsgBean._meta.get_fields()]
    fill_fields = {key: value for key, value in python_obj.items() if key in model_fields and value is not None}
    
    fill_fields['userid'] = request.user.get('user_id')
    fill_fields = {
        (key + '_id') if key in ["userid"] else key: value
        for key, value in fill_fields.items()
    }

    
    fill_fields['cd'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        
    
    

    

    Sysmsg.SysmsgBean.objects.create(**fill_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()



def removeSysmsgById(request):

    Sysmsg.SysmsgBean.objects.filter(id=request.GET.get("id")).delete()
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=1)
    return response_data.to_json_response()


def updateSysmsgById(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    id = request.GET.get("id")
    # 获取请求中传递的字段及其值，过滤掉不在Sysmsg中的字段
    model_fields = [f.name for f in Sysmsg.SysmsgBean._meta.get_fields()]
    fill_fields = {key: value for key, value in python_obj.items() if key in model_fields and value is not None}
    
    fill_fields['userid'] = request.user.get('user_id')
    fill_fields = {
        (key + '_id') if key in ["userid"] else key: value
        for key, value in fill_fields.items()
    }

    
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        

    # 更新Sysmsg信息，仅更新传递的字段
    Sysmsg.SysmsgBean.objects.filter(id=id).update(**fill_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()


def getSysmsg(request):
    
   
    page = int(request.GET.get("pg", 1))
    limit = int(request.GET.get("limit", 10))
    

    data_dict = {}
    msuserid = request.GET.get("msuserid","")
    mstitle = request.GET.get("mstitle","")
    mscontent = request.GET.get("mscontent","")
    msstatus = request.GET.get("msstatus","")
    mstype = request.GET.get("mstype","")
    userid = request.GET.get("userid","")
    cd = request.GET.get("cd","")
    md = request.GET.get("md","")
    
    if msuserid:
        data_dict["msuserid"] = msuserid
    if mstitle:
        data_dict["mstitle__contains"] = mstitle
    if msstatus:
        data_dict["msstatus"] = msstatus
    if mstype:
        data_dict["mstype__contains"] = mstype
    if userid:
        data_dict["userid"] = userid
    if cd:
        data_dict["cd_gte"] = cd
    if md:
        data_dict["md_gte"] = md
    queryset = Sysmsg.SysmsgBean.objects.filter(**data_dict).order_by("-id")
    
  
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
        
        userid = getattr(item, 'userid_id', None) 
        
        user_name = ""
        avatar = ""
            
            
        if userid:
            try:
                
                user_name = item.userid.user_name if item.userid else ""
                avatar = item.userid.avatar if item.userid else ""
            except Exception:  # 捕获所有可能的异常
                
                user_name = ""
                avatar = ""

            
        data_list.append({
            'id': item.id,
            'msuserid': item.msuserid,
            'mstitle': item.mstitle,
            'mscontent': item.mscontent,
            'msstatus': item.msstatus,
            'mstype': item.mstype,
            'userid': userid,
            'username': user_name,
            'useravatar': avatar,
            'cd': item.cd,
            'md': item.md,
        })

    # 替换序列化好的数据
    del data['objects_list']
    data['data'] = data_list
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=data)
    return response_data.to_json_response()
    


def getSysmsgById(request):

    # 从请求参数中获取 id
    
    data_dict = {}
    msuserid = request.GET.get("msuserid","")
    mstitle = request.GET.get("mstitle","")
    mscontent = request.GET.get("mscontent","")
    msstatus = request.GET.get("msstatus","")
    mstype = request.GET.get("mstype","")
    userid = request.GET.get("userid","")
    cd = request.GET.get("cd","")
    md = request.GET.get("md","")
    
    id = request.GET.get("id")
    if id:
        data_dict["id"] = id
    
    if msuserid:
        data_dict["msuserid"] = msuserid
    if mstitle:
        data_dict["mstitle__contains"] = mstitle
    if msstatus:
        data_dict["msstatus"] = msstatus
    if mstype:
        data_dict["mstype__contains"] = mstype
    if userid:
        data_dict["userid"] = userid
    if cd:
        data_dict["cd_gte"] = cd
    if md:
        data_dict["md_gte"] = md
    queryset = Sysmsg.SysmsgBean.objects.filter(**data_dict).order_by("-id")
    item =Sysmsg.SysmsgBean.objects.filter(**data_dict).first()
    if not item:
        return ResponseJsonData(errcode=500, errmsg='没有数据', retobj='业务错误')
    # 从数据库中获取到一个对象 item
    
    userid = getattr(item, 'userid_id', None) 
    
    user_name = ""
    avatar = ""
        
        
    if userid:
        try:
            
            user_name = item.userid.user_name if item.userid else ""
            avatar = item.userid.avatar if item.userid else ""
        except Exception:  # 捕获所有可能的异常
            
            user_name = ""
            avatar = ""

        
    result = {
        'id': item.id,
            'msuserid': item.msuserid,
            'mstitle': item.mstitle,
            'mscontent': item.mscontent,
            'msstatus': item.msstatus,
            'mstype': item.mstype,
            'userid': userid,
            'username': user_name,
            'useravatar': avatar,
            'cd': item.cd,
            'md': item.md,
    }
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=result)
    return response_data.to_json_response()

