from django.db.models import Q
from django_filters.rest_framework.filterset import FilterSet

from ..import models
from django_filters import filters



class project_FilterSet(FilterSet):
    # 区间查询,指定区间的最大最小值
    # min_price = filters.NumberFilter (field_name='price', lookup_expr='gte')  # gte lte 源码里面有，表示最大最小值
    # max_price = filters.NumberFilter (field_name='price', lookup_expr='lte')
    # 模糊查询,这里带i是忽略大小写
    # name = filters.CharFilter (field_name="name", lookup_expr="icontains")
    sort = filters.OrderingFilter(fields=('id',))
    class Meta:
        model = models.Project_info
        fields = "__all__"


class Account_project_FilterSet(FilterSet):
    # 区间查询,指定区间的最大最小值
    # min_price = filters.NumberFilter (field_name='price', lookup_expr='gte')  # gte lte 源码里面有，表示最大最小值
    # max_price = filters.NumberFilter (field_name='price', lookup_expr='lte')
    # 模糊查询,这里带i是忽略大小写
    # name = filters.CharFilter (field_name="name", lookup_expr="icontains")
    class Meta:
        model = models.Account_project
        fields = ['project_name','expense_name','finish_flag']

class UserInfo_FilterSet(FilterSet):
    query = filters.CharFilter (field_name="name", lookup_expr="icontains")
    class Meta:
        model = models.UserInfo
        fields = ['query',]

class Account_normal_FilterSet(FilterSet):
    class Meta:
        model = models.Account_normal
        fields = ['project_name', 'expense_name', 'finish_flag']

class Account_view_FilterSet(FilterSet):
    # query=filters.CharFilter(field_name='project_name__project_name', lookup_expr="icontains")

    query = filters.CharFilter(method='filter_case',lookup_expr="icontains")
    timelte = filters.CharFilter(field_name='account_date',lookup_expr="lte")
    timegte = filters.CharFilter(field_name='account_date',lookup_expr="gte")
    #query = filters.CharFilter(field_name="project_name", lookup_expr="icontains")
    # query = filters.CharFilter(field_name="cause", lookup_expr="icontains")
    #records = query1 | query2
    # def filter_time(self,queryset,name,value):
    #     return queryset.filter(Q(account_date__gte=value[0])&Q(account_date__lte=value[1]))
    def filter_case(self,queryset,name,value):
        return queryset.filter(Q(project_name__project_name__icontains=value)|Q(cause__icontains=value))
    class Meta:
        model = models.Account_view
        fields = ['query','project_name', 'expense_name', 'finish_flag','type','timelte','timegte']

class Contract_info_FilterSet(FilterSet):
    searchyear = filters.DateFilter(method='filter_searchyear')
    query = filters.CharFilter(method='filter_case',lookup_expr="icontains")
    def filter_searchyear(self,queryset,name,value):
        year = format(value, '%Y')
        return queryset.filter(Q(Date_start__year=year))
    def filter_case(self,queryset,name,value):
        return queryset.filter(Q(project__project_name__icontains=value)|Q(explain__icontains=value)|Q(contract_name__icontains=value))
    class Meta:
        model = models.Contract_info
        fields = ['project', 'contract_type','query','searchyear']

class Cotract_plan_FilerSet(FilterSet):
    class Meta:
        model =  models.Contract_plan
        fields = '__all__'
