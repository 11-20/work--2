
from django.db import models
from work.bean.Role import RoleBean  # 根据实际的文件结构调整导入路径

class UserBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    id = models.AutoField(primary_key=True)
    user_name =  models.CharField(verbose_name="用户名", max_length=100)
    avatar =  models.CharField(verbose_name="用户头像", max_length=100)
    phone =  models.CharField(verbose_name="手机号", max_length=100)
    email =  models.CharField(verbose_name="邮箱", max_length=100)
    password =  models.CharField(verbose_name="密码", max_length=100)
    sex =  models.IntegerField(verbose_name="性别", max_length=100)
    status =  models.IntegerField(verbose_name="状态", max_length=100)
    remark =  models.CharField(verbose_name="备注", max_length=100)
    is_super =  models.IntegerField(verbose_name="是否最高权限", max_length=100)

    # 外键：所属角色
    role_id = models.ForeignKey(RoleBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="role_id")
    class Meta:
        db_table = 'user' # 通过db_table自定义数据表名

