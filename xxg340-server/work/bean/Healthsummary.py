
from django.db import models
from work.bean.User import UserBean

class HealthsummaryBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    hs_date = models.CharField(verbose_name="统计日期", max_length=100)
    hs_type = models.CharField(verbose_name="统计类型", max_length=100)
    hs_avgbmi = models.CharField(verbose_name="平均BMI", max_length=100)
    hs_avgsbp = models.CharField(verbose_name="平均收缩压", max_length=100)
    hs_avgdbp = models.CharField(verbose_name="平均舒张压", max_length=100)
    hs_avgchol = models.CharField(verbose_name="平均总胆固醇", max_length=100)
    hs_highriskrate = models.CharField(verbose_name="高风险比例", max_length=100)
    hs_normalrate = models.CharField(verbose_name="正常指标比例", max_length=100)
    hs_summarydata = models.TextField(verbose_name="汇总数据JSON")
    userid = models.IntegerField(verbose_name="用户id")
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    # 外键：关联用户
    userid = models.ForeignKey(UserBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="userid")
    class Meta:
        db_table = 'healthsummary' # 通过db_table自定义数据表名

