
from django.db import models
from work.bean.User import UserBean

class PredictionmodelBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    pm_filepath = models.TextField(verbose_name="模型文件路径")
    pm_dataset = models.TextField(verbose_name="训练数据集描述")
    pm_status = models.IntegerField(verbose_name="模型状态")
    pm_description = models.TextField(verbose_name="模型描述")
    wywpm_name = models.CharField(verbose_name="模型名称", max_length=100)
    nubpm_version = models.CharField(verbose_name="模型版本", max_length=100)
    userid = models.IntegerField(verbose_name="用户id")
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    # 外键：关联用户
    userid = models.ForeignKey(UserBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="userid")
    class Meta:
        db_table = 'predictionmodel' # 通过db_table自定义数据表名

