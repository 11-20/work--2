
from work.bean import Healthdata
from django.shortcuts import HttpResponse
from django.core import serializers
import json
from work.utils.Pagination import  Custom_Paginator
from django.http import JsonResponse
from work.utils.ResponseJson import ResponseJsonData   
from datetime import datetime



def createHealthdata(request):
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    if 'id' in python_obj:
        del python_obj['id']

    # 获取请求中传递的字段及其值，过滤掉不在Healthdata中的字段
    model_fields = [f.name for f in Healthdata.HealthdataBean._meta.get_fields()]
    fill_fields = {key: value for key, value in python_obj.items() if key in model_fields and value is not None}
    
    fill_fields['userid'] = request.user.get('user_id')
    fill_fields = {
        (key + '_id') if key in ["userid"] else key: value
        for key, value in fill_fields.items()
    }

    
    fill_fields['cd'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        
    
    

    

    Healthdata.HealthdataBean.objects.create(**fill_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()



def removeHealthdataById(request):

    Healthdata.HealthdataBean.objects.filter(id=request.GET.get("id")).delete()
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=1)
    return response_data.to_json_response()


def updateHealthdataById(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    id = request.GET.get("id")
    # 获取请求中传递的字段及其值，过滤掉不在Healthdata中的字段
    model_fields = [f.name for f in Healthdata.HealthdataBean._meta.get_fields()]
    fill_fields = {key: value for key, value in python_obj.items() if key in model_fields and value is not None}
    
    fill_fields['userid'] = request.user.get('user_id')
    fill_fields = {
        (key + '_id') if key in ["userid"] else key: value
        for key, value in fill_fields.items()
    }

    
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        

    # 更新Healthdata信息，仅更新传递的字段
    Healthdata.HealthdataBean.objects.filter(id=id).update(**fill_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()


def getHealthdata(request):
    
   
    page = int(request.GET.get("pg", 1))
    limit = int(request.GET.get("limit", 10))
    

    data_dict = {}
    hd_date = request.GET.get("hd_date","")
    hd_weight = request.GET.get("hd_weight","")
    hd_height = request.GET.get("hd_height","")
    hd_bmi = request.GET.get("hd_bmi","")
    hd_sbp = request.GET.get("hd_sbp","")
    hd_dbp = request.GET.get("hd_dbp","")
    hd_glucose = request.GET.get("hd_glucose","")
    hd_cholesterol = request.GET.get("hd_cholesterol","")
    hd_hdl = request.GET.get("hd_hdl","")
    hd_ldl = request.GET.get("hd_ldl","")
    hd_triglycerides = request.GET.get("hd_triglycerides","")
    hd_smoking = request.GET.get("hd_smoking","")
    hd_exercise = request.GET.get("hd_exercise","")
    hd_alcohol = request.GET.get("hd_alcohol","")
    userid = request.GET.get("userid","")
    cd = request.GET.get("cd","")
    md = request.GET.get("md","")
    
    if hd_date:
        data_dict["hd_date__contains"] = hd_date
    if hd_weight:
        data_dict["hd_weight__contains"] = hd_weight
    if hd_height:
        data_dict["hd_height__contains"] = hd_height
    if hd_bmi:
        data_dict["hd_bmi__contains"] = hd_bmi
    if hd_sbp:
        data_dict["hd_sbp__contains"] = hd_sbp
    if hd_dbp:
        data_dict["hd_dbp__contains"] = hd_dbp
    if hd_glucose:
        data_dict["hd_glucose__contains"] = hd_glucose
    if hd_cholesterol:
        data_dict["hd_cholesterol__contains"] = hd_cholesterol
    if hd_hdl:
        data_dict["hd_hdl__contains"] = hd_hdl
    if hd_ldl:
        data_dict["hd_ldl__contains"] = hd_ldl
    if hd_triglycerides:
        data_dict["hd_triglycerides"] = hd_triglycerides
    if hd_smoking:
        data_dict["hd_smoking"] = hd_smoking
    if hd_exercise:
        data_dict["hd_exercise__contains"] = hd_exercise
    if hd_alcohol:
        data_dict["hd_alcohol"] = hd_alcohol
    if userid:
        data_dict["userid"] = userid
    if cd:
        data_dict["cd_gte"] = cd
    if md:
        data_dict["md_gte"] = md
    queryset = Healthdata.HealthdataBean.objects.filter(**data_dict).order_by("-id")
    
  
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
            'hd_date': item.hd_date,
            'hd_weight': item.hd_weight,
            'hd_height': item.hd_height,
            'hd_bmi': item.hd_bmi,
            'hd_sbp': item.hd_sbp,
            'hd_dbp': item.hd_dbp,
            'hd_glucose': item.hd_glucose,
            'hd_cholesterol': item.hd_cholesterol,
            'hd_hdl': item.hd_hdl,
            'hd_ldl': item.hd_ldl,
            'hd_triglycerides': item.hd_triglycerides,
            'hd_smoking': item.hd_smoking,
            'hd_exercise': item.hd_exercise,
            'hd_alcohol': item.hd_alcohol,
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
    


def getHealthdataById(request):

    # 从请求参数中获取 id
    
    data_dict = {}
    hd_date = request.GET.get("hd_date","")
    hd_weight = request.GET.get("hd_weight","")
    hd_height = request.GET.get("hd_height","")
    hd_bmi = request.GET.get("hd_bmi","")
    hd_sbp = request.GET.get("hd_sbp","")
    hd_dbp = request.GET.get("hd_dbp","")
    hd_glucose = request.GET.get("hd_glucose","")
    hd_cholesterol = request.GET.get("hd_cholesterol","")
    hd_hdl = request.GET.get("hd_hdl","")
    hd_ldl = request.GET.get("hd_ldl","")
    hd_triglycerides = request.GET.get("hd_triglycerides","")
    hd_smoking = request.GET.get("hd_smoking","")
    hd_exercise = request.GET.get("hd_exercise","")
    hd_alcohol = request.GET.get("hd_alcohol","")
    userid = request.GET.get("userid","")
    cd = request.GET.get("cd","")
    md = request.GET.get("md","")
    
    id = request.GET.get("id")
    if id:
        data_dict["id"] = id
    
    if hd_date:
        data_dict["hd_date__contains"] = hd_date
    if hd_weight:
        data_dict["hd_weight__contains"] = hd_weight
    if hd_height:
        data_dict["hd_height__contains"] = hd_height
    if hd_bmi:
        data_dict["hd_bmi__contains"] = hd_bmi
    if hd_sbp:
        data_dict["hd_sbp__contains"] = hd_sbp
    if hd_dbp:
        data_dict["hd_dbp__contains"] = hd_dbp
    if hd_glucose:
        data_dict["hd_glucose__contains"] = hd_glucose
    if hd_cholesterol:
        data_dict["hd_cholesterol__contains"] = hd_cholesterol
    if hd_hdl:
        data_dict["hd_hdl__contains"] = hd_hdl
    if hd_ldl:
        data_dict["hd_ldl__contains"] = hd_ldl
    if hd_triglycerides:
        data_dict["hd_triglycerides"] = hd_triglycerides
    if hd_smoking:
        data_dict["hd_smoking"] = hd_smoking
    if hd_exercise:
        data_dict["hd_exercise__contains"] = hd_exercise
    if hd_alcohol:
        data_dict["hd_alcohol"] = hd_alcohol
    if userid:
        data_dict["userid"] = userid
    if cd:
        data_dict["cd_gte"] = cd
    if md:
        data_dict["md_gte"] = md
    queryset = Healthdata.HealthdataBean.objects.filter(**data_dict).order_by("-id")
    item =Healthdata.HealthdataBean.objects.filter(**data_dict).first()
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
            'hd_date': item.hd_date,
            'hd_weight': item.hd_weight,
            'hd_height': item.hd_height,
            'hd_bmi': item.hd_bmi,
            'hd_sbp': item.hd_sbp,
            'hd_dbp': item.hd_dbp,
            'hd_glucose': item.hd_glucose,
            'hd_cholesterol': item.hd_cholesterol,
            'hd_hdl': item.hd_hdl,
            'hd_ldl': item.hd_ldl,
            'hd_triglycerides': item.hd_triglycerides,
            'hd_smoking': item.hd_smoking,
            'hd_exercise': item.hd_exercise,
            'hd_alcohol': item.hd_alcohol,
            'userid': userid,
            'username': user_name,
            'useravatar': avatar,
            'cd': item.cd,
            'md': item.md,
    }
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=result)
    return response_data.to_json_response()

