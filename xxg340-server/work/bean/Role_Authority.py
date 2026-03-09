
from django.db import models
class Role_AuthorityBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    id = models.AutoField(primary_key=True)
    roleId =  models.IntegerField(verbose_name="角色ID", max_length=100)
    perId =  models.IntegerField(verbose_name="权限ID", max_length=100)
    class Meta:
        db_table = 'role_authority' # 通过db_table自定义数据表名

