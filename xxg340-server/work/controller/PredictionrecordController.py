
from work.bean import Predictionrecord
from django.shortcuts import HttpResponse
from django.core import serializers
import json
from work.utils.Pagination import  Custom_Paginator
from django.http import JsonResponse
from work.utils.ResponseJson import ResponseJsonData   
from datetime import datetime



def createPredictionrecord(request):
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    if 'id' in python_obj:
        del python_obj['id']

    # 获取请求中传递的字段及其值，过滤掉不在Predictionrecord中的字段
    model_fields = [f.name for f in Predictionrecord.PredictionrecordBean._meta.get_fields()]
    fill_fields = {key: value for key, value in python_obj.items() if key in model_fields and value is not None}
    
    fill_fields['userid'] = request.user.get('user_id')
    fill_fields = {
        (key + '_id') if key in ["pm_id","userid"] else key: value
        for key, value in fill_fields.items()
    }

    
    fill_fields['cd'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        
    
    

    

    Predictionrecord.PredictionrecordBean.objects.create(**fill_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()



def removePredictionrecordById(request):

    Predictionrecord.PredictionrecordBean.objects.filter(id=request.GET.get("id")).delete()
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=1)
    return response_data.to_json_response()


def updatePredictionrecordById(request):
    # 获取请求体中的 JSON 字符串
    json_string = request.body.decode('utf-8')
    # 将 JSON 字符串转换为 Python 对象
    python_obj = json.loads(json_string)
    id = request.GET.get("id")
    # 获取请求中传递的字段及其值，过滤掉不在Predictionrecord中的字段
    model_fields = [f.name for f in Predictionrecord.PredictionrecordBean._meta.get_fields()]
    fill_fields = {key: value for key, value in python_obj.items() if key in model_fields and value is not None}
    
    fill_fields['userid'] = request.user.get('user_id')
    fill_fields = {
        (key + '_id') if key in ["pm_id","userid"] else key: value
        for key, value in fill_fields.items()
    }

    
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_fields['md'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        

    # 更新Predictionrecord信息，仅更新传递的字段
    Predictionrecord.PredictionrecordBean.objects.filter(id=id).update(**fill_fields)
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=python_obj)
    return response_data.to_json_response()


def getPredictionrecord(request):
    
   
    page = int(request.GET.get("pg", 1))
    limit = int(request.GET.get("limit", 10))
    

    data_dict = {}
    pm_id = request.GET.get("pm_id","")
    pr_age = request.GET.get("pr_age","")
    pr_sex = request.GET.get("pr_sex","")
    pr_cp = request.GET.get("pr_cp","")
    pr_trestbps = request.GET.get("pr_trestbps","")
    pr_chol = request.GET.get("pr_chol","")
    pr_fbs = request.GET.get("pr_fbs","")
    pr_restecg = request.GET.get("pr_restecg","")
    pr_thalach = request.GET.get("pr_thalach","")
    pr_exang = request.GET.get("pr_exang","")
    pr_oldpeak = request.GET.get("pr_oldpeak","")
    pr_slope = request.GET.get("pr_slope","")
    pr_ca = request.GET.get("pr_ca","")
    pr_thal = request.GET.get("pr_thal","")
    pr_risklevel = request.GET.get("pr_risklevel","")
    pr_probability = request.GET.get("pr_probability","")
    pr_predictiontime = request.GET.get("pr_predictiontime","")
    pr_batchfile = request.GET.get("pr_batchfile","")
    pr_resultfile = request.GET.get("pr_resultfile","")
    pr_isbatch = request.GET.get("pr_isbatch","")
    userid = request.GET.get("userid","")
    cd = request.GET.get("cd","")
    md = request.GET.get("md","")
    
    if pm_id:
        data_dict["pm_id"] = pm_id
    if pr_age:
        data_dict["pr_age__contains"] = pr_age
    if pr_sex:
        data_dict["pr_sex"] = pr_sex
    if pr_cp:
        data_dict["pr_cp__contains"] = pr_cp
    if pr_trestbps:
        data_dict["pr_trestbps__contains"] = pr_trestbps
    if pr_chol:
        data_dict["pr_chol__contains"] = pr_chol
    if pr_fbs:
        data_dict["pr_fbs__contains"] = pr_fbs
    if pr_restecg:
        data_dict["pr_restecg__contains"] = pr_restecg
    if pr_thalach:
        data_dict["pr_thalach__contains"] = pr_thalach
    if pr_exang:
        data_dict["pr_exang__contains"] = pr_exang
    if pr_oldpeak:
        data_dict["pr_oldpeak__contains"] = pr_oldpeak
    if pr_slope:
        data_dict["pr_slope__contains"] = pr_slope
    if pr_ca:
        data_dict["pr_ca__contains"] = pr_ca
    if pr_thal:
        data_dict["pr_thal__contains"] = pr_thal
    if pr_risklevel:
        data_dict["pr_risklevel__contains"] = pr_risklevel
    if pr_probability:
        data_dict["pr_probability__contains"] = pr_probability
    if pr_predictiontime:
        data_dict["pr_predictiontime__contains"] = pr_predictiontime
    if pr_isbatch:
        data_dict["pr_isbatch"] = pr_isbatch
    if userid:
        data_dict["userid"] = userid
    if cd:
        data_dict["cd_gte"] = cd
    if md:
        data_dict["md_gte"] = md
    queryset = Predictionrecord.PredictionrecordBean.objects.filter(**data_dict).order_by("-id")
    
  
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
        
        pm_id = getattr(item, 'pm_id_id', None) 
        
        wywpm_name = ""
        nubpm_version = ""
            
            
        if pm_id:
            try:
                
                wywpm_name = item.pm_id.wywpm_name if item.pm_id else ""
                nubpm_version = item.pm_id.nubpm_version if item.pm_id else ""
            except Exception:  # 捕获所有可能的异常
                
                wywpm_name = ""
                nubpm_version = ""

            
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
            'pm_id': pm_id,
            'wywpm_name': wywpm_name,
            'nubpm_version': nubpm_version,
            'pr_age': item.pr_age,
            'pr_sex': item.pr_sex,
            'pr_cp': item.pr_cp,
            'pr_trestbps': item.pr_trestbps,
            'pr_chol': item.pr_chol,
            'pr_fbs': item.pr_fbs,
            'pr_restecg': item.pr_restecg,
            'pr_thalach': item.pr_thalach,
            'pr_exang': item.pr_exang,
            'pr_oldpeak': item.pr_oldpeak,
            'pr_slope': item.pr_slope,
            'pr_ca': item.pr_ca,
            'pr_thal': item.pr_thal,
            'pr_risklevel': item.pr_risklevel,
            'pr_probability': item.pr_probability,
            'pr_predictiontime': item.pr_predictiontime,
            'pr_batchfile': item.pr_batchfile,
            'pr_resultfile': item.pr_resultfile,
            'pr_isbatch': item.pr_isbatch,
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
    


def getPredictionrecordById(request):

    # 从请求参数中获取 id
    
    data_dict = {}
    pm_id = request.GET.get("pm_id","")
    pr_age = request.GET.get("pr_age","")
    pr_sex = request.GET.get("pr_sex","")
    pr_cp = request.GET.get("pr_cp","")
    pr_trestbps = request.GET.get("pr_trestbps","")
    pr_chol = request.GET.get("pr_chol","")
    pr_fbs = request.GET.get("pr_fbs","")
    pr_restecg = request.GET.get("pr_restecg","")
    pr_thalach = request.GET.get("pr_thalach","")
    pr_exang = request.GET.get("pr_exang","")
    pr_oldpeak = request.GET.get("pr_oldpeak","")
    pr_slope = request.GET.get("pr_slope","")
    pr_ca = request.GET.get("pr_ca","")
    pr_thal = request.GET.get("pr_thal","")
    pr_risklevel = request.GET.get("pr_risklevel","")
    pr_probability = request.GET.get("pr_probability","")
    pr_predictiontime = request.GET.get("pr_predictiontime","")
    pr_batchfile = request.GET.get("pr_batchfile","")
    pr_resultfile = request.GET.get("pr_resultfile","")
    pr_isbatch = request.GET.get("pr_isbatch","")
    userid = request.GET.get("userid","")
    cd = request.GET.get("cd","")
    md = request.GET.get("md","")
    
    id = request.GET.get("id")
    if id:
        data_dict["id"] = id
    
    if pm_id:
        data_dict["pm_id"] = pm_id
    if pr_age:
        data_dict["pr_age__contains"] = pr_age
    if pr_sex:
        data_dict["pr_sex"] = pr_sex
    if pr_cp:
        data_dict["pr_cp__contains"] = pr_cp
    if pr_trestbps:
        data_dict["pr_trestbps__contains"] = pr_trestbps
    if pr_chol:
        data_dict["pr_chol__contains"] = pr_chol
    if pr_fbs:
        data_dict["pr_fbs__contains"] = pr_fbs
    if pr_restecg:
        data_dict["pr_restecg__contains"] = pr_restecg
    if pr_thalach:
        data_dict["pr_thalach__contains"] = pr_thalach
    if pr_exang:
        data_dict["pr_exang__contains"] = pr_exang
    if pr_oldpeak:
        data_dict["pr_oldpeak__contains"] = pr_oldpeak
    if pr_slope:
        data_dict["pr_slope__contains"] = pr_slope
    if pr_ca:
        data_dict["pr_ca__contains"] = pr_ca
    if pr_thal:
        data_dict["pr_thal__contains"] = pr_thal
    if pr_risklevel:
        data_dict["pr_risklevel__contains"] = pr_risklevel
    if pr_probability:
        data_dict["pr_probability__contains"] = pr_probability
    if pr_predictiontime:
        data_dict["pr_predictiontime__contains"] = pr_predictiontime
    if pr_isbatch:
        data_dict["pr_isbatch"] = pr_isbatch
    if userid:
        data_dict["userid"] = userid
    if cd:
        data_dict["cd_gte"] = cd
    if md:
        data_dict["md_gte"] = md
    queryset = Predictionrecord.PredictionrecordBean.objects.filter(**data_dict).order_by("-id")
    item =Predictionrecord.PredictionrecordBean.objects.filter(**data_dict).first()
    if not item:
        return ResponseJsonData(errcode=500, errmsg='没有数据', retobj='业务错误')
    # 从数据库中获取到一个对象 item
    
    pm_id = getattr(item, 'pm_id_id', None) 
    
    wywpm_name = ""
    nubpm_version = ""
        
        
    if pm_id:
        try:
            
            wywpm_name = item.pm_id.wywpm_name if item.pm_id else ""
            nubpm_version = item.pm_id.nubpm_version if item.pm_id else ""
        except Exception:  # 捕获所有可能的异常
            
            wywpm_name = ""
            nubpm_version = ""

        
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
            'pm_id': pm_id,
            'wywpm_name': wywpm_name,
            'nubpm_version': nubpm_version,
            'pr_age': item.pr_age,
            'pr_sex': item.pr_sex,
            'pr_cp': item.pr_cp,
            'pr_trestbps': item.pr_trestbps,
            'pr_chol': item.pr_chol,
            'pr_fbs': item.pr_fbs,
            'pr_restecg': item.pr_restecg,
            'pr_thalach': item.pr_thalach,
            'pr_exang': item.pr_exang,
            'pr_oldpeak': item.pr_oldpeak,
            'pr_slope': item.pr_slope,
            'pr_ca': item.pr_ca,
            'pr_thal': item.pr_thal,
            'pr_risklevel': item.pr_risklevel,
            'pr_probability': item.pr_probability,
            'pr_predictiontime': item.pr_predictiontime,
            'pr_batchfile': item.pr_batchfile,
            'pr_resultfile': item.pr_resultfile,
            'pr_isbatch': item.pr_isbatch,
            'userid': userid,
            'username': user_name,
            'useravatar': avatar,
            'cd': item.cd,
            'md': item.md,
    }
    response_data = ResponseJsonData(errcode=0, errmsg='success', retobj=result)
    return response_data.to_json_response()

