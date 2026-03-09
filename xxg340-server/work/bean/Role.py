
from django.db import models
class RoleBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(verbose_name="角色名", max_length=100)
    status = models.IntegerField(verbose_name="状态", max_length=100)
    remark = models.CharField(verbose_name="备注", max_length=100)
    class Meta:
        db_table = 'role' # 通过db_table自定义数据表名

