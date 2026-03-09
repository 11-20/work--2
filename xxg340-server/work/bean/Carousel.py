
from django.db import models
from work.bean.User import UserBean

class CarouselBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    ca_title = models.CharField(verbose_name="轮播图标题", max_length=100)
    ca_cover = models.TextField(verbose_name="轮播图图片")
    ca_excerpt = models.TextField(verbose_name="轮播图简介")
    userid = models.IntegerField(verbose_name="用户id")
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    # 外键：关联用户
    userid = models.ForeignKey(UserBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="userid")
    class Meta:
        db_table = 'carousel' # 通过db_table自定义数据表名

