
from django.db import models
class AuthorityBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    id = models.AutoField(primary_key=True)
    parentId =  models.IntegerField(verbose_name="父级ID", max_length=100)
    perName =  models.CharField(verbose_name="权限名称", max_length=100)
    path =  models.CharField(verbose_name="节点路径", max_length=100)
    perUrl =  models.CharField(verbose_name="页面路径", max_length=100)
    perIcon =  models.CharField(verbose_name="权限图标", max_length=100)
    class Meta:
        db_table = 'authority' # 通过db_table自定义数据表名

