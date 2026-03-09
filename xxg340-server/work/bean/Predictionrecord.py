
from django.db import models
from work.bean.Predictionmodel import PredictionmodelBean
from work.bean.User import UserBean

class PredictionrecordBean(models.Model):
    # bean 里面的所有属性对应数据库里面的字段
    
    id = models.AutoField(primary_key=True)
    pr_age = models.CharField(verbose_name="年龄", max_length=100)
    pr_sex = models.IntegerField(verbose_name="性别")
    pr_cp = models.CharField(verbose_name="胸痛类型", max_length=100)
    pr_trestbps = models.CharField(verbose_name="静息血压", max_length=100)
    pr_chol = models.CharField(verbose_name="血清胆固醇", max_length=100)
    pr_fbs = models.CharField(verbose_name="空腹血糖", max_length=100)
    pr_restecg = models.CharField(verbose_name="静息心电图结果", max_length=100)
    pr_thalach = models.CharField(verbose_name="最大心率", max_length=100)
    pr_exang = models.CharField(verbose_name="运动诱发心绞痛", max_length=100)
    pr_oldpeak = models.CharField(verbose_name="ST段压低", max_length=100)
    pr_slope = models.CharField(verbose_name="ST段峰值运动斜率", max_length=100)
    pr_ca = models.CharField(verbose_name="主要血管数量", max_length=100)
    pr_thal = models.CharField(verbose_name="地中海贫血", max_length=100)
    pr_risklevel = models.CharField(verbose_name="风险等级", max_length=100)
    pr_probability = models.CharField(verbose_name="预测概率", max_length=100)
    pr_predictiontime = models.CharField(verbose_name="预测时间", max_length=100)
    pr_batchfile = models.TextField(verbose_name="批量预测文件")
    pr_resultfile = models.TextField(verbose_name="预测结果文件")
    pr_isbatch = models.IntegerField(verbose_name="是否批量预测")
    userid = models.IntegerField(verbose_name="用户id")
    cd = models.CharField(verbose_name="创建时间", max_length=100)
    md = models.CharField(verbose_name="更新时间", max_length=100)
    # 外键：使用的预测模型
    pm_id = models.ForeignKey(PredictionmodelBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="pm_id")
    # 外键：关联用户
    userid = models.ForeignKey(UserBean,to_field="id",on_delete=models.CASCADE, null=True, blank=True,db_column="userid")
    class Meta:
        db_table = 'predictionrecord' # 通过db_table自定义数据表名

