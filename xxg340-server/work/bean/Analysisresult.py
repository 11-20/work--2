
from django.db import models
from work.bean.User import UserBean

class AnalysisresultBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    ar_type = models.CharField(verbose_name="分析类型", max_length=100)
    ar_resultdata = models.TextField(verbose_name="结果数据")
    ar_summary = models.TextField(verbose_name="分析摘要")
    ar_period = models.CharField(verbose_name="统计周期", max_length=100)
    ar_generatedate = models.CharField(verbose_name="生成日期", max_length=100)
    userid = models.IntegerField(verbose_name="用户id")
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    # 外键：关联用户
    userid = models.ForeignKey(UserBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="userid")
    class Meta:
        db_table = 'analysisresult' # 通过db_table自定义数据表名

