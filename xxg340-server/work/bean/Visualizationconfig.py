
from django.db import models
from work.bean.User import UserBean

class VisualizationconfigBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    vc_name = models.CharField(verbose_name="配置名称", max_length=100)
    vc_charttype = models.CharField(verbose_name="图表类型", max_length=100)
    vc_datamodel = models.CharField(verbose_name="数据模型", max_length=100)
    vc_fields = models.TextField(verbose_name="关联字段")
    vc_timefilter = models.CharField(verbose_name="时间范围", max_length=100)
    vc_filter = models.TextField(verbose_name="筛选条件")
    vc_isdefault = models.IntegerField(verbose_name="是否默认配置")
    userid = models.IntegerField(verbose_name="用户id")
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    # 外键：关联用户
    userid = models.ForeignKey(UserBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="userid")
    class Meta:
        db_table = 'visualizationconfig' # 通过db_table自定义数据表名

