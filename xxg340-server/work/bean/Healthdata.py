
from django.db import models
from work.bean.User import UserBean

class HealthdataBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    hd_date = models.CharField(verbose_name="记录日期", max_length=100)
    hd_weight = models.CharField(verbose_name="体重(kg)", max_length=100)
    hd_height = models.CharField(verbose_name="身高(cm)", max_length=100)
    hd_bmi = models.CharField(verbose_name="BMI指数", max_length=100)
    hd_sbp = models.CharField(verbose_name="收缩压", max_length=100)
    hd_dbp = models.CharField(verbose_name="舒张压", max_length=100)
    hd_glucose = models.CharField(verbose_name="血糖水平", max_length=100)
    hd_cholesterol = models.CharField(verbose_name="总胆固醇", max_length=100)
    hd_hdl = models.CharField(verbose_name="高密度脂蛋白", max_length=100)
    hd_ldl = models.CharField(verbose_name="低密度脂蛋白", max_length=100)
    hd_triglycerides = models.CharField(verbose_name="甘油三酯", max_length=100)
    hd_smoking = models.IntegerField(verbose_name="是否吸烟")
    hd_exercise = models.CharField(verbose_name="每周运动时长(小时)", max_length=100)
    hd_alcohol = models.IntegerField(verbose_name="是否饮酒")
    userid = models.IntegerField(verbose_name="用户id")
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    # 外键：关联用户
    userid = models.ForeignKey(UserBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="userid")
    class Meta:
        db_table = 'healthdata' # 通过db_table自定义数据表名

