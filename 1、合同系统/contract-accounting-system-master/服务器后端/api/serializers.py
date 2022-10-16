from django.utils import timezone
from rest_framework import serializers

from api import models
from api.models import UserInfo, Test, Department, Entity_info, Project_info, Traffic_type, Account_project, \
    Account_normal, Account_view, Contract_plan, Contract_info, attachment


# class UserstestSerializer(serializers.ModelSerializer):
#     department = serializers.ReadOnlyField (source='department.dept_name')
#
#     # brand = serializers.SlugRelatedField(read_only=True ,slug_field='name') ①
#     # brand = serializers.StringRelatedField(label='类别') ②
#     class Meta:
#         model = UserInfo
#         fields = "__all__"
#

#用户信息
class UserSerializer(serializers.HyperlinkedModelSerializer):
    user_type_choices = (
        (1, "普通用户"),
        (2, "管理员"),
    )
    #user_type = serializers.CharField(source='get_user_type_display') 这个是在枚举中选中的值直接显示
    dept_name = serializers.ReadOnlyField(source='department.dept_name') #这里的department是指mode中的字段名
    department_id = serializers.IntegerField(required=False,allow_null=True)
    # abc = serializers.ReadOnlyField(source='user_type_choices') 这个可以自定义想要传送的对象
    # stutstxt =  serializers.HyperlinkedIdentityField(view_name='tt', lookup_field='id', lookup_url_kwarg='pk')
    class Meta:
        model = UserInfo
        #exclude = ()
        fields = ['url','id','user_type','username','password','status','department_id','name',"dept_name"]

        # fields = "__all__"

class TestSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ['url','name']
#部门信息
class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    dept_manager_id = serializers.IntegerField (required=False, allow_null=True)
    dept_manager_name = serializers.ReadOnlyField(source='dept_manager.name')
    class Meta:
        model = Department
        fields = ['url','id','dept_name','dept_manager_id','dept_manager_name']
#交通方式
class TrafficSerializer (serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Traffic_type
        fields = ['url','id','project_name']

#全局修改
class AccountQGlistSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        for index, obj in enumerate (instance):
            self.child.update (obj, validated_data[index])
        return instance

#项目出差报销记帐表
class AccountSerializer (serializers.ModelSerializer):
    expense_name = serializers.HiddenField(default=serializers.CurrentUserDefault())
    finish_flag = serializers.HiddenField(default=0)
    start_date = serializers.DateField (format="%Y-%m-%d")
    end_date = serializers.DateField (format="%Y-%m-%d")
    type_traffic_name = serializers.ReadOnlyField (source='Type_traffic.project_name')
    # account_date = serializers.HiddenField(default=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    account_date = serializers.DateTimeField (format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    approve_id = serializers.IntegerField (required=False, allow_null=True)
    approvetime = serializers.DateTimeField (format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = Account_project
        fields = "__all__"


        #list_serializer_class = AccountQGlistSerializer

#报销查询
class AccountlistSerializer(serializers.ModelSerializer):
    account_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    pj_name = serializers.ReadOnlyField(source='project_name.project_name')
    user = serializers.ReadOnlyField(source='expense_name.name')   #models里用户报销表的报销人.user info中的name
    zhushu = serializers.DecimalField(max_digits=10,decimal_places=2,coerce_to_string = False)
    money_traffic = serializers.DecimalField(max_digits=10,decimal_places=2,coerce_to_string = False)
    sumButie = serializers.DecimalField(max_digits=10, decimal_places=2,coerce_to_string = False)
    jtfs = serializers.ReadOnlyField(source='Type_traffic.project_name')
    approve_id = serializers.IntegerField (required=False, allow_null=True)
    approve_user = serializers.ReadOnlyField(source='approve.name')
    approvetime = serializers.DateTimeField (format="%Y-%m-%d %H:%M:%S", required=False)
    class Meta:
        model = Account_project
        fields = ['id','pj_name','user','project_name','start_addr','end_addr','expense_name','zhushu','jtfs','Type_traffic','money_traffic','sumDate','sumButie','start_date','end_date','account_date','explain','finish_flag','approve_id','approvetime','approve_user']
        list_serializer_class = AccountQGlistSerializer
        #extra_kwargs = {'pj_name'}
        #exclude = ()
    # def __init__(self, *args, **kwargs):
    #     user = kwargs['context']['request'].user
    #     super (AccountSerializer, self).__init__ (*args, **kwargs)
    #     self.fields['owner'].default = user
    #     self.fields['parent'].queryset = Account_project.objects.filter (owner=user)

#其他报销
class Account_normalSerializer(serializers.ModelSerializer):
    project_name_id = serializers.IntegerField(required=False,allow_null=True)
    expense_name = serializers.HiddenField(default=serializers.CurrentUserDefault())
    account_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    finish_flag = serializers.HiddenField(default=0)
    approve_id = serializers.IntegerField(required=False,allow_null=True)
    approvetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",required=False, read_only=True)
    class Meta:
        model = Account_normal
        fields = "__all__"

#其他报销查询
class normallistSerializer(serializers.ModelSerializer):
    pj_name = serializers.ReadOnlyField(source='project_name.project_name')
    account_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.ReadOnlyField(source='expense_name.name')
    approve_id = serializers.IntegerField (required=False, allow_null=True)
    approve_user = serializers.ReadOnlyField(source='approve.name')
    approvetime = serializers.DateTimeField (format="%Y-%m-%d %H:%M:%S", required=False)
    class Meta:
        model = Account_normal
        fields = ['id','user','pj_name','expense_name','date','account_date','money','cause','project_name','finish_flag','approve_id','approvetime','approve_user']
        list_serializer_class = AccountQGlistSerializer

#单位信息
class EntitySerializer (serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField ( )
    entity_addr = serializers.CharField(required=False,allow_blank=True)
    phone = serializers.CharField(required=False,allow_blank=True)
    bank_addr = serializers.CharField(required=False,allow_blank=True)
    bank_number = serializers.CharField(required=False,allow_blank=True)
    shuiHao = serializers.CharField(required=False,allow_blank=True)
    explain = serializers.CharField(required=False,allow_blank=True)
    def get_id(self, instance):
        return instance.id
    class Meta:
        model = Entity_info
        read_only_fields = ["id"]
        fields = "__all__"
        exclude = []

 #项目信息
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    customer_id=serializers.IntegerField ()
    owner_id=serializers.IntegerField ()
    customer_name= serializers.CharField(source='customer.entity_name',read_only=True)
    owner_name = serializers.CharField(source='owner.entity_name',read_only=True)

    class Meta:
        model = Project_info
        # read_only_fields = ["id"]
        # fields = "__all__"
        # exclude = []
        fields = ['url','id','customer_id','owner_id','project_name','customer_name','owner_name']

#查询视图
class Account_viewSerializer(serializers.ModelSerializer):
     account_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
     user =  serializers.ReadOnlyField(source='expense_name.name')   #models里用户报销表的报销人.user info中的name
     pj_name = serializers.ReadOnlyField(source='project_name.project_name')
#     project_name_id = serializers.IntegerField(required=False, allow_null=True)
#     tableid = serializers.CharField(max_length=64)
#     cause = serializers.CharField(max_length=64)
     money = serializers.DecimalField(max_digits=10, decimal_places=2,coerce_to_string = False)
     class Meta:
        model = Account_view
        fields = ['type','sysid','expense_name','tableid','project_name','cause','money','account_date','finish_flag','user','pj_name']

# #全局修改
# class viewListSerializer(serializers.ListSerializer):
#     def update(self, instance, validated_data):
#         # print(instance)  # 要更新的对象们
#         # print(validated_data)  # 更新的对象对应的数据们
#         # print(self.child)  # 服务的模型序列化类 - V2BookModelSerializer
#         for index, obj in enumerate(instance):
#             self.child.update(obj, validated_data[index])
#         return instance

#附件
class attachmentSerializer(serializers.ModelSerializer):
    filename = serializers.ReadOnlyField()
    class Meta:
        model = attachment
        # read_only_fields = ["id"]
        # fields = "__all__"
        fields = ['id','file','hetong','filename']

#合同信息
class Contract_infoSerializer(serializers.ModelSerializer):
    #contract_name = serializers.CharField(required=False,allow_blank=True)
    project_name = serializers.ReadOnlyField(source='project.project_name')
    Date_start = serializers.DateField(format="%Y-%m-%d")
    Date_end = serializers.DateField(format="%Y-%m-%d", required=False)
    taxes = serializers.DecimalField(required=False,allow_null=True,max_digits=10,decimal_places=2,coerce_to_string = False)
    explain = serializers.CharField(required=False,allow_blank=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,coerce_to_string = False)
    attchments = attachmentSerializer(many=True,read_only=True)
    zj_percent=serializers.SerializerMethodField()
    fp_percent=serializers.SerializerMethodField()
    # attachment = serializers.ListField(
    #     allow_null=True,
    #     child=serializers.FileField(max_length=None,allow_empty_file=False, ))
    #attachment = serializers.SerializerMethodField()
    # attachment = serializers.SlugRelatedField(many=True, slug_field='file', queryset=models.attachment.objects.all(), allow_null=True)
    # attachment = serializers.ManyRelatedField(serializers.SlugRelatedField(slug_field='file',source='attachment_id',queryset=models.attachment.objects.all()),)
    # attachment = serializers.ManyRelatedField(required=False,allow_null=True,child_relation=serializers.SlugRelatedField(slug_field='file',source='attachment_id',queryset=models.attachment.objects.all()))
    # def get_attachment(self,obj):
    #     query_set = models.attachment.objects.all()
    #     return [{'file_name':obj.file} for obj in query_set]

    class Meta:
        model = Contract_info
        fields = ['id','project_name','project','contract_name','contract_type','amount','body','target','Date_start','Date_end','taxes','explain','attchments','zj_percent','fp_percent']
    def get_zj_percent(self,obj):
        s = 0
        #查询该合同对应的所有资金计划
        query_set = models.Contract_plan.objects.filter(contractinfo_id=obj.id,contract_type=1)
        for infoObj in query_set:
            if infoObj.finish_type == '1':
                s +=  round ((infoObj.money_plan / obj.amount)* 100,2)
        return s
    def get_fp_percent(self,obj):
        s = 0
        # 查询该合同对应的所有发票计划
        query_set = models.Contract_plan.objects.filter (contractinfo_id=obj.id, contract_type=0)
        for infoObj in query_set:
            if infoObj.finish_type == '1':
                s += round ((infoObj.money_plan / obj.amount) * 100,2 )
        return s
#合同账务计划
class Contract_planSerializer(serializers.ModelSerializer):
    # contract_id =serializers.IntegerField ()
    date_plan = serializers.DateField(format="%Y-%m-%d", required=False)
    money_plan = serializers.DecimalField(max_digits=10, decimal_places=2,coerce_to_string = False)
    xiangmu = serializers.ReadOnlyField(source='contract.project')
    class Meta:
        model = Contract_plan
        fields = ['id','xiangmu','contractinfo','date_plan','money_plan','contract_type','finish_type']
