from django.db import models

# Create your models here.

'''
    该文件用于定义自身所需的数据库
    在django中将数据库表的操作定义为特殊的类
    表的字段对应数据库中类的属性
    类的方法用于对数据的增删改查
    
    ---若更换数据库 直接修改相关配置项即可实现 ORM object relational mapping
    使用db_index建立索引
'''

'''
************************************
************************************
*****      以下为关系实体表       *****
************************************
************************************
'''


class SeaSurfaceHeight(models.Model):
    no = models.AutoField(primary_key=True)
    date = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    ssh = models.FloatField(null=True)


'''
    身份信息表:
'''


class IdentityInfo(models.Model):
    # 客户账号 主键
    no = models.IntegerField(primary_key=True, db_index=True)
    # 客户密码
    password = models.CharField(max_length=20)
    # 客户属于 'V' 'S' 'Q'
    belong = models.CharField(max_length=1, db_index=True)


'''
    服务台人员表
'''


class QueryAssist(models.Model):
    # 咨询人员账号 主键 设定为identity_info的外码
    no = models.OneToOneField(
        IdentityInfo, on_delete=models.CASCADE, primary_key=True, db_index=True)
    # 咨询人员姓名
    name = models.CharField(max_length=20)
    # 在线状态
    state = models.CharField(max_length=2)


'''
    访客表
'''


class Visitor(models.Model):
    # 访客账号 主键 设定为identity_info的外码
    no = models.OneToOneField(
        IdentityInfo, on_delete=models.CASCADE, primary_key=True, db_index=True)
    # 访客姓名
    name = models.CharField(max_length=20)
    # 访客年龄
    v_age = models.IntegerField()
    # 访客性别 'male' 'female'
    v_gender = models.CharField(max_length=6)
    # 访客病史
    v_aim = models.CharField(max_length=100)


'''
    工作人员表
'''


class Staff(models.Model):
    # 工作人员账号 主键 设定为identity_info的外码
    no = models.OneToOneField(
        IdentityInfo, on_delete=models.CASCADE, primary_key=True, db_index=True)
    # 工作人员姓名
    name = models.CharField(max_length=20)
    # 工作人员职称 'expert' 'normal'
    s_profession = models.CharField(max_length=60)
    # 工作人员专业科室
    s_depart = models.CharField(max_length=20, db_index=True)
    # 综合评分指数
    s_index = models.DecimalField(max_digits=10, decimal_places=2)
    # 开始时间
    s_time_begin = models.IntegerField()
    # 结束时间
    s_time_end = models.IntegerField()


'''
    授权表
'''


class Dataset(models.Model):
    # 名称 主键
    d_name = models.CharField(max_length=20, primary_key=True, db_index=True)
    # 描述
    d_presc = models.CharField(max_length=100)


'''
    分数表
'''


class Score(models.Model):
    # 评分编号 主键
    f_no = models.IntegerField(primary_key=True, db_index=True)
    # 评分的具体数值
    f_score = models.IntegerField()
    # 评分时间
    f_time = models.DateTimeField()
    # 评分针对的工作人员编号 外码
    no = models.ForeignKey(Staff, on_delete=models.CASCADE, db_index=True)


'''
    意见表
'''


class Comment(models.Model):
    # 意见编号 主键
    cc_no = models.IntegerField(primary_key=True, db_index=True)
    # 意见内容
    cc_content = models.CharField(max_length=100)
    # 反馈时间
    cc_time = models.DateTimeField()
    # 意见针对的医生编号 外码
    no = models.ForeignKey(Staff, on_delete=models.CASCADE, db_index=True)


'''
************************************
************************************
*****      以下为实体间关系表      *****
************************************
************************************
'''

'''
    申请与工作人员间的关系： 当前到号信息
    二者为多对多的关系
'''


class Current_Apply(models.Model):
    # 当前到号号码
    a_index = models.IntegerField(db_index=True)
    # 当前日期
    a_date = models.DateField(db_index=True)
    # 当前工作人员编号
    a_no_staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, db_index=True, null=True)


'''
    顾客与工作人员间的关系： 申请表
    二者为多对多的关系
'''


class Apply(models.Model):
    # 申请号码
    a_index = models.IntegerField(db_index=True)
    # 申请日期
    a_date = models.DateField(db_index=True)
    # 与Staff表是多对多的关系
    a_no_staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, db_index=True, null=True)
    # 与Visitor表是多对多的关系
    a_no_visitor = models.ForeignKey(
        Visitor, on_delete=models.CASCADE, db_index=True, null=True)


'''
    顾客与服务台咨询人员的关系：交流表
    二者为多对多的关系
'''


class Communication(models.Model):
    # 发送者编号
    cs_no = models.ForeignKey(
        IdentityInfo, on_delete=models.CASCADE, db_index=True, related_name="cs")
    # 接收者编号
    cr_no = models.ForeignKey(
        IdentityInfo, on_delete=models.CASCADE, db_index=True, related_name="cr")
    # 发生信息日期
    cs_time = models.DateField(db_index=True)
    # 信息内容
    content = models.CharField(max_length=100)


'''
    顾客与数据集的关系：授权表
    二者为多对多的关系
'''


class Authorization(models.Model):
    # 药物名称
    d_name = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, db_index=True)
    # 药物数量
    Au_num = models.IntegerField()
    # 患者编号
    Au_no = models.ManyToManyField(Visitor)
    # 挂号号码
    Au_index = models.IntegerField(db_index=True)
    # 挂号日期
    Au_date = models.DateField(db_index=True)


'''
    顾客与评分的关系：评分反馈表
    二者为多对一的关系
'''


class ScoreFeedback(models.Model):
    # 评分编号
    f_no = models.OneToOneField(Score, on_delete=models.CASCADE, db_index=True)
    # 访客编号
    no = models.ManyToManyField(Visitor)


'''
    访客与意见关系：意见反馈表
    二者为多对一的关系
'''


class CommentFeedback(models.Model):
    # 意见编号
    cc_no = models.OneToOneField(
        Comment, on_delete=models.CASCADE, db_index=True)
    no = models.ManyToManyField(Visitor)


class Permission(models.Model):
    # 权限编号
    p_index = models.IntegerField(primary_key=True)
    # 用户编号
    p_no = models.CharField(max_length=2)
    # 权限说明
    p_depict = models.CharField(max_length=100)
