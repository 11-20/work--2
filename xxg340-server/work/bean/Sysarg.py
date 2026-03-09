
from django.db import models

class SysargBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    confkey = models.CharField(verbose_name="配置键名", max_length=100)
    confname = models.CharField(verbose_name="配置名称", max_length=100)
    confvalue = models.TextField(verbose_name="配置值")
    conftype = models.CharField(verbose_name="配置类型", max_length=100)
    confdesc = models.CharField(verbose_name="配置描述", max_length=100)
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    class Meta:
        db_table = 'sysarg' # 通过db_table自定义数据表名

