
from django.db import models
from work.bean.User import UserBean

class SyslogBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    logstitle = models.CharField(verbose_name="日志标题", max_length=100)
    logip = models.CharField(verbose_name="客户端标识", max_length=100)
    loglevel = models.CharField(verbose_name="日志级别", max_length=100)
    logcontent = models.TextField(verbose_name="日志内容")
    userid = models.IntegerField(verbose_name="用户id")
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    # 外键：关联用户
    userid = models.ForeignKey(UserBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="userid")
    class Meta:
        db_table = 'syslog' # 通过db_table自定义数据表名

