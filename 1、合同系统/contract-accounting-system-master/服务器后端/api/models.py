import os

from django.db import models

# Create your models here.
from django.db.models import ForeignKey, AutoField
from django.db.models.functions import datetime

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)
    class Meta:
        managed = False
        db_table = 'home'
class Test(models.Model):
    name = models.CharField(max_length=20)

#用户信息表
class UserInfo(models.Model):
    user_type_choices = (
        (1,"普通用户"),
        (2,"管理员"),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=32,unique=True,default="无名氏")
    status = models.BooleanField(default=True)
    department = models.ForeignKey(to="Department",on_delete=models.SET_NULL,null=True)
    #
    # @property
    # def department_dept_name(self):
    #     return self.department.dept_name

#用户令牌表
class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo',on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

#职能部门表
class Department(models.Model):
    dept_name = models.CharField(max_length=64,unique=True,blank=False,default="技术部")
    dept_manager = models.ForeignKey(to="UserInfo",on_delete=models.SET_NULL,null=True,related_name="dep_manager_user")



#工程项目表
class Project_info(models.Model):
    project_name = models.CharField(max_length=64,unique=True,blank=False)#项目名称
    customer = models.ForeignKey(to="Entity_info",on_delete=models.PROTECT,related_name="project_customer")#项目的客户名
    owner = models.ForeignKey(to="Entity_info",on_delete=models.PROTECT,related_name="project_owner")#项目所属公司


#单位信息表
class Entity_info(models.Model):
    entity_name = models.CharField(max_length=128,unique=True,blank=False)#单位名称
    entity_addr = models.CharField(max_length=128,null=True)#单位地址
    phone = models.CharField(max_length=32,null=True)#单位电话
    bank_addr = models.CharField(max_length=64,null=True)
    bank_number = models.CharField(max_length=64,null=True)#银行帐号
    shuiHao = models.CharField(max_length=64,null=True)#税号
    explain = models.CharField(max_length=64,null=True)#备注

#合同信息表
class Contract_info(models.Model):
    contract_type_choices = (
        (1, "收款合同"),
        (2, "付款合同"),
    )
    project = models.ForeignKey(to="Project_info",on_delete=models.PROTECT) #项目信息
    contract_name = models.CharField(max_length=64)#合同名称
    contract_type = models.CharField(max_length=64,choices=contract_type_choices) #合同类型
    amount = models.DecimalField(max_digits=10,decimal_places=2) #合同金额
    body = models.ForeignKey (to="Entity_info", on_delete=models.PROTECT,related_name="body_entity")  # 合同本方
    target = models.ForeignKey (to="Entity_info", on_delete=models.PROTECT)#合同对方
    Date_start = models.DateField()#签订日期
    Date_end = models.DateField(null=True)#合同到期日期
    attachment =models.ManyToManyField("attachment",verbose_name=u'附件',null=True)
    taxes = models.DecimalField(max_digits=10,decimal_places=2,null=True) #税金成本
    explain = models.CharField(max_length=64,null=True)#备注

#合同财务计划表
class Contract_plan(models.Model):
    type_choices = (
        (0, "发票类型/未完成"),
        (1, "资金类型/已完成"),
    )
    contractinfo = models.ForeignKey(to="Contract_info",on_delete=models.CASCADE) #对应的合同,合同删除计划也被删除
    date_plan = models.DateField() # 计划日期
    money_plan = models.DecimalField(max_digits=10,decimal_places=2) # 计划金额project_name
    contract_type = models.CharField(max_length=64,choices=type_choices)#计划类型
    finish_type = models.CharField(max_length=64,choices=type_choices)#完成款情况

#交通方式
class Traffic_type(models.Model):
    project_name = models.CharField (max_length=64,unique=True, blank=False)


#补贴表
class Subsidize_info(models.Model):
    Department = models.ForeignKey (to="Department", on_delete=models.SET_NULL,null=True)
    money = models.DecimalField(max_digits=5,decimal_places=2) #金额天

#项目出差报销记帐表
class Account_project(models.Model):
    finish_flag_choices = (
        (0, "未完成报销"),
        (1, "已完成报销"),
    )
    expense_name = models.ForeignKey(to="UserInfo",on_delete=models.PROTECT)#报销人
    project_name = models.ForeignKey(to="Project_info",on_delete=models.PROTECT,null=True)#所属项目
    start_addr = models.CharField(max_length=64)
    end_addr = models.CharField(max_length=64)
    zhushu = models.DecimalField(max_digits=10,decimal_places=2) #住宿金额
    Type_traffic = models.ForeignKey(to="Traffic_type",on_delete=models.PROTECT)#交通方式
    money_traffic = models.DecimalField(max_digits=10,decimal_places=2) #交通费
    sumDate = models.IntegerField()#天数
    sumButie = models.DecimalField(max_digits=10, decimal_places=2,)  # 总补贴费
    start_date = models.DateField(null=True) #开始日期
    end_date = models.DateField(null=True) #结束日期
    account_date = models.DateTimeField(blank=True, auto_now_add=True, null=True)  # 报销日期
    explain = models.CharField(max_length=64) #备注 (在serializers.py里面设置运行为空)
    finish_flag = models.CharField(max_length=64,choices=finish_flag_choices,default=finish_flag_choices[0][0]) #完成情况(在serializers.py里面设置运行为空)
    approve = models.ForeignKey(to="UserInfo",on_delete=models.PROTECT,related_name="Accountproject_approve_user",null=True)#审批人
    approvetime = models.DateTimeField(null=True,blank=True,) #审批时间

#用户判断
#class User_judgment(models.Model):
    #user = models.CharField(max_length=32,unique=True)

#其他报销
class Account_normal(models.Model):
    finish_flag_choices = (
        (0, "未完成报销"),
        (1, "已完成报销"),
    )
    expense_name = models.ForeignKey (to="UserInfo",on_delete=models.PROTECT)  # 报销人
    date = models.DateField() #发生日期
    account_date = models.DateTimeField(blank=True,auto_now_add=True,null=True)  # 报销日期
    money = models.DecimalField(max_digits=10 ,decimal_places=2)  # 金额
    cause = models.CharField(max_length=64,blank=False) #报销内容
    project_name = models.ForeignKey (to="Project_info",null=True,on_delete=models.PROTECT)  # 所属项目
    finish_flag = models.CharField (max_length=64,choices=finish_flag_choices, default=finish_flag_choices[0][0])  # 完成情况
    approve = models.ForeignKey(to="UserInfo", on_delete=models.PROTECT,related_name="Accountnormal_approve_user",null=True)  # 审批人
    approvetime = models.DateTimeField(null=True,blank=True,) #审批时间

def get_file_path(instance,filename):
    return 'files/合同附件/'+str(instance.hetong.id)+'/'+filename

#附件表
class attachment(models.Model):
    # file_name = models.CharField(max_length=64)
    # file = models.FileField(max_length=100,upload_to="files/")
    file = models.FileField(max_length=100,upload_to=get_file_path)
    hetong = models.ForeignKey(to="Contract_info",on_delete=models.CASCADE,related_name='attchments')#反向查询时候要用到这个related_name
    #attachment = models.CharField(max_length=128, null=True)
    def filename(self):
        return os.path.basename (self.file.name)
#查询视图
class Account_view(models.Model):
    type = models.CharField(max_length=2)  # 类型
    sysid = models.CharField(primary_key=True,max_length=64)
    expense_name = models.ForeignKey(to="UserInfo", on_delete=models.PROTECT)  # 报销人
    tableid = models.IntegerField(max_length=32)
    project_name = models.ForeignKey(to="Project_info", on_delete=models.PROTECT) #所属项目
    cause = models.CharField(max_length=64, blank=False)  # 报销事由
    money = models.DecimalField(max_digits=10, decimal_places=2)  # 金额
    account_date = models.DateTimeField(blank=True, auto_now_add=True, null=True)  # 报销日期
    finish_flag = models.IntegerField()# 完成情况

    class Meta:
        db_table = 'account_view'
