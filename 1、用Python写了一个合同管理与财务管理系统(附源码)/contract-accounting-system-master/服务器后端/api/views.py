from django.db.models.functions import datetime
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
from api.utils import auth

from api import models, serializers
from api.models import Test

# Create your views here.
from api.serializers import UserSerializer, TestSerializer, DepartmentSerializer, EntitySerializer, ProjectSerializer, \
    TrafficSerializer, AccountSerializer, Account_normalSerializer, AccountlistSerializer, normallistSerializer, \
    Account_viewSerializer, Contract_planSerializer, Contract_infoSerializer, attachmentSerializer
from api.utils import httpback
from api.utils.auth import ApiPermission2, IsOwnerOrReadOnly, IsOwnerOrReadOnlyForAccount, \
    IsOwnerOrReadOnlyForAccountView, IsAdminOrReadOnly, IsAdminOrReadOnlyForUser
from api.utils import config
from api.utils.httpback import HttpCode
from api.utils.myfilters import Account_project_FilterSet, UserInfo_FilterSet, Account_normal_FilterSet, \
    Account_view_FilterSet, Contract_info_FilterSet, Cotract_plan_FilerSet, project_FilterSet
from api.utils.pageutils import MyPageNumberPagination
from django.conf import settings

def index(request):
    return HttpResponseRedirect ("/api")


# 测试数据库操作
def testdb(request):
    test1 = Test (name='liu008.com')
    test1.save ( )
    return HttpResponse ("<p>数据添加成功！</p>")


from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions, viewsets


#########################REST API 验证
class MyAuthentication (BasicAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get ('token')
        if not token:
            raise exceptions.AuthenticationFailed ('用户认证失败')
        return {"alex", None}

    def authenticate_header(self, val):
        pass


class DogView (APIView):
    # authentication_classes = [MyAuthentication, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': 'xxxxx'}
        return HttpResponse (json.dumps (ret), status=201)


##########数据库查表认证
def md5(user):
    import hashlib
    import time

    ctime = str (time.time ( ))
    m = hashlib.md5 (bytes (user, encoding='utf-8'))
    m.update (bytes (ctime, encoding='utf-8'))
    return m.hexdigest ( )


##---------------------登录验证
class Login (APIView):
    authentication_classes = []  # 列表里写入验证类，为空代表不需要验证

    # permission_classes = [ApiPermission] #列表里写入权限控制类
    # parser_classes = [FileUploadParser] #单独指定解析器
    def post(self, request, *args, **kwargs):
        # self.dispatch()
        ret = {'data': {'email': None, 'id': None, 'mobile': None, 'rid': None, 'token': None, 'username': None,
                        'name': None},
               'meta': {'msg': "", 'status': 200}}
        try:
            data = request.data
            user = data['username']
            pwd = data['password']
            print("用户名为:" + user + "想来登录")
            # print ("用户名为:" + user + "想来登录")
            obj = models.UserInfo.objects.filter (username=user, password=pwd).first ( )

            if not obj:  # 如果取不出
                ret['meta']['status'] = 1001
                ret['meta']['msg'] = "用户名密码错误"
                return JsonResponse (ret)
            token = md5 (user)
            # 在数据表中写入或更新token
            print (user + "登录成功")
            models.UserToken.objects.update_or_create (user=obj, defaults={'token': token})
            ret['data']['token'] = token
            ret['data']['id'] = obj.id
            ret['data']['name'] = obj.name
        except Exception as e:
            print(e)
            ret['meta']['status'] = 1001
            ret['meta']['msg'] = "请求异常"
        return JsonResponse (ret)

#通过token取个人信息
@api_view(http_method_names=['POST'])
def getUserInfo(request):
    data = request.data
    token = data['token']
    try:
        if not len(token)==0:#如果有token
            print("token有值")
            print(token+"999")
            user = models.UserToken.objects.filter (token=token).first()
            if user:#如果有返回用户
                user = user.user#查询数据并通过外键关键拿到用户对象
            else:
                return httpback.params_error(message="别乱拿假数据过来！")
            ul = UserSerializer(user,context={'request': request})
            data = ul.data
        else:
            return httpback.params_error(message="you have no token!")
    except Exception as e:
        # print(e)
        return httpback.server_error( )

    return httpback.result(data=data,message="ok")



class ZhuChe(APIView):
    authentication_classes = []  # 列表里写入验证类，为空代表不需要验证
    def get(self,request):
        hostid = config.getHostid()
        license =config.getLicense()
        if license =="":
            msg = "not register"
        else:
            if(config.init(license)):
                msg = "registered"
            else:
                msg = "not register"

        return httpback.result(data={'hostid':hostid,'license':license},message=msg)

    def post(self,request, *args, **kwargs):
        try:
            data = request.data
            license = data['license']
            if config.init(license):
                #写入license
                config.putLicense(license)
                return httpback.result(message='ok')
            else:
                return httpback.result(code=HttpCode.paramserror,message="注册码有误")
        except Exception as e:
            # print(e)
            return httpback.server_error ( )
class TestData (APIView):
    permission_classes = [ApiPermission2]

    def get(self, request):
        ret = {
            "key01": "vaule01",
            "key02": "vaule02",
            "key03": "vaule03",
        }
        return JsonResponse (ret)


# 获取用户主菜单
# class GetMenus (APIView):
#     def get(self, request):
#         menu = {
#             "data": [
#                 {
#                     "id": 101,
#                     "authName": "用户管理",
#                     "path": "/user",
#                     "children": [
#                         {
#                             "id": 102,
#                             "authName": "用户列表",
#                             "path": None,
#                             "children": []
#                         }
#                     ]
#                 },
#                 {
#                     "id": 201,
#                     "authName": "权限管理",
#                     "path": None,
#                     "children": [
#                         {
#                             "id": 202,
#                             "authName": "权限管理",
#                             "path": None,
#                             "children": []
#                         }
#                     ]
#
#                 }
#             ],
#             "meta": {
#                 "msg": "获取菜单列表成功",
#                 "status": 200
#             }
#         }
#         return JsonResponse (menu)

#用户不分页
class UserAllViewSet(viewsets.ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnlyForUser, ]
    # filter_backends = (DjangoFilterBackend, ) 可以全局配置，所以此处不再配置
    filter_class = UserInfo_FilterSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserInfo.objects.all()
    pagination_class = MyPageNumberPagination
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnlyForUser, ]
    # filter_backends = (DjangoFilterBackend, ) 可以全局配置，所以此处不再配置
    filter_class = UserInfo_FilterSet
    # search_fields = ('query', )
    # 核心部分就是list方法
    # def list(self, request):
    #     keyword = request.GET.get ('query')  # 获取参数
    #     print(keyword)
    #     if keyword is not None:  # 如果参数不为空
    #         # 执行filter()方法
    #         queryset = models.UserInfo.objects.filter (name__contains=keyword)#在name字段找关键字
    #     else:
    #         # 如果参数为空，执行all()方法
    #         queryset = models.UserInfo.objects.all ( )
    #     #serializer = UserSerializer (queryset, many=True)
    #     page =  MyPageNumberPagination()
    #     page_roles =page.paginate_queryset(queryset,request)
    #     serializer = UserSerializer (page_roles, context={'request': request}, many=True)
    #     #serializer = UserSerializer (instance=page_roles, many=True)
    #     return page.get_paginated_response(serializer.data)  # 最后返回经过序列化的数据





class TestViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.all()
    serializer_class = TestSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly, ]
#单位
class EntityViewSet(viewsets.ModelViewSet):
    queryset = models.Entity_info.objects.all()
    serializer_class = EntitySerializer
    pagination_class = MyPageNumberPagination

#单位不分页
class EntityAllViewSet(viewsets.ModelViewSet):
    queryset = models.Entity_info.objects.all()
    serializer_class = EntitySerializer


# class UsertestViewSet(viewsets.ModelViewSet):
#     queryset = models.UserInfo.objects.all()
#     serializer_class = UserstestSerializer

#项目
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project_info.objects.all().order_by('-id')#排序一下，后建立的项目排前面
    serializer_class = ProjectSerializer
    pagination_class = MyPageNumberPagination
    filter_class = project_FilterSet
#项目不分页
class ProjectAllViewSet(viewsets.ModelViewSet):
    queryset = models.Project_info.objects.all().order_by('-id')#排序一下，后建立的项目排前面
    serializer_class = ProjectSerializer
    filter_class = project_FilterSet

#交通方式
class TrafficViewSet(viewsets.ModelViewSet):
    queryset = models.Traffic_type.objects.all()
    serializer_class = TrafficSerializer

#项目出差报销记帐表
class AccountViewSet(viewsets.ModelViewSet):
    queryset = models.Account_project.objects.all()
    ##serializer_class = AccountSerializer
    pagination_class = MyPageNumberPagination
    permission_classes = [IsOwnerOrReadOnlyForAccount, ]
    # serializer_class =AccountSerializer
    # filter_backends = [DjangoFilterBackend]
    filter_class = Account_project_FilterSet
    serializers_class = Example_SERIALIZERS_DICT = {
        'list': AccountlistSerializer,
        'create': AccountSerializer,
        'update': AccountSerializer,
        'retrieve': AccountlistSerializer,
        'partial_update': AccountSerializer
    }

    # def get_queryset(self):
    #     # queryset = self.queryset
    #     my = self.request.query_params.get('mylist',0)
    #     if my:
    #         user = self.request.user
    #         queryset = Account_project.objects.filter(expense_name = user)
    #         return queryset
    #     return models.Account_project.objects.all()

    def get_serializer_class(self):
        try:
            return self.serializers_class[self.action]
        except KeyError:
            raise     # 处理不可对应的情况

    # 群局部改（单局部改）：请求数据 -[{pk：1，name=123}，{pk:2,name=456},{pk:8,price:666}]
    def patch(self, request, *args, **kwargs):
        request_data = request.data  # 数据包数据
        print(request.user)
        # pk = request_data.get ('pk')
        # 将单改，群改的数据都格式化成 pks=[要需要的对象主键标识] | request_data=[每个要修改的对象对应的修改数据]
        # if pk and isinstance (request_data, dict):  # 单改
        #     pks = [pk, ]
        #     request_data = [request_data, ]
        if isinstance (request_data, list):  # 群改
            pks = []
            # 遍历前台数据[{pk:1, name:123}, {pk:3, price:7}, {pk:7, publish:2}]，拿一个个字典
            for dic in request_data:
                pk = dic.pop ('pk', None)  # 返回pk值
                if pk:
                    pks.append (pk)
                # pk没有传值
                else:
                    return Response ({
                        'status': 1,
                        'msg': '参数错误'
                    })
        else:
            return Response ({
                'status': 1,
                'msg': '参数错误'
            })
        # pks与request_data数据筛选，
        # 1）将pks中的没有对应数据的pk与数据已删除的pk移除，request_data对应索引位上的数据也移除
        # 2）将合理的pks转换为 objs
        objs = []
        new_request_data = []
        for index, pk in enumerate (pks):
            try:
                # 将pk合理的对象数据保存下来
                book_obj = models.Account_project.objects.get (id=pk)
                objs.append (book_obj)
                # 对应索引的数据也保存下来,并且加人审批人和审批时间
                spobj = request_data[index]
                # spobj.approve_id = request.user
                # spobj.approvetime = datetime.datetime.now()
                spobj.update(approve_id=request.user.id)
                spobj.update(approvetime=datetime.datetime.now())
                new_request_data.append (spobj)
                # spobj = {'approve_id': user}
                # spobj.update(approve_id = user)
                # print(spobj)
            except Exception as ex :
                print(ex)
                # 重点：反面教程 - pk对应的数据有误，将对应索引的data中request_data中移除
                # 在for循环中不要使用删除
                # index = pks.index(pk)
                # request_data.pop(index)
                continue
        # 生成一个serializer对象
        try:
            book_ser = serializers.AccountlistSerializer (instance=objs, data=new_request_data, partial=True, many=True)
            book_ser.is_valid (raise_exception=True)
            book_objs = book_ser.save ( )
            return Response ({
                'status': 200,
                'msg': 'ok',
                'results': serializers.AccountlistSerializer (book_objs, many=True).data
            })
        except Exception as ex :
            print(ex)
            return Response ({
                'status': 501,
                'msg': 'err',
                'results': serializers.AccountlistSerializer (book_objs, many=True).data
            })
        #     new_params = list()
        #     # 直接获取 body(请求体, 二进制数据), 解码后, 进行切割
        #     for param in request.body.decode(encoding="utf-8").split("&"):
        #         if "approve_id" in param:
        #             # 修改参数值, 并重新拼接参数
        #             new_str = "approve_id=" + param.split("=")[1].replace("-", " ")
        #             new_params.append(new_str)
        #         else:
        #             new_params.append(param)
        #     # 重新构造请求体, 进行编码后, 重新赋值给 request._body
        #     # 注意: 是 request._body, 因为 request.body 是不可修改的, 但是 body 属性继承自 _body 属性, 所以直接修改 _body 属性
        #     request._body = "&".join(new_params).encode(encoding="utf-8")
        #
        # ...
        #
        # def params_replace(self, data):
        #     # 按需求, 对请求参数中的值做出修改
        #     name = data.patch("approve_id")
        #     if name:
        #         data["pprove_id"] = name.replace("-", " ")
        #         return data
        #     else:
        #         return None


#非项目出差报销
class Account_normalViewSet(viewsets.ModelViewSet):
    queryset = models.Account_normal.objects.all()
    #serializer_class = Account_normalSerializer
    pagination_class = MyPageNumberPagination
    permission_classes = [IsOwnerOrReadOnlyForAccount, ]
    filter_class = Account_normal_FilterSet
    serializers_class = Example_SERIALIZERS_DICT = {
        'list': normallistSerializer,
        'create': Account_normalSerializer,
        'update': Account_normalSerializer,
        'retrieve': normallistSerializer,
        'partial_update': Account_normalSerializer
    }
    def get_serializer_class(self):
        try:
            return self.serializers_class[self.action]
        except KeyError:
            raise     # 处理不可对应的情况
    def patch(self, request, *args, **kwargs):
        request_data = request.data  # 数据包数据
        # pk = request_data.get ('pk')
        # 将单改，群改的数据都格式化成 pks=[要需要的对象主键标识] | request_data=[每个要修改的对象对应的修改数据]
        # if pk and isinstance (request_data, dict):  # 单改
        #     pks = [pk, ]
        #     request_data = [request_data, ]
        if isinstance (request_data, list):  # 群改
            pks = []
            # 遍历前台数据[{pk:1, name:123}, {pk:3, price:7}, {pk:7, publish:2}]，拿一个个字典
            for dic in request_data:
                pk = dic.pop ('pk', None)  # 返回pk值
                if pk:
                    pks.append (pk)
                # pk没有传值
                else:
                    return Response ({
                        'status': 1,
                        'msg': '参数错误'
                    })
        else:
            return Response ({
                'status': 1,
                'msg': '参数错误'
            })
        # pks与request_data数据筛选，
        # 1）将pks中的没有对应数据的pk与数据已删除的pk移除，request_data对应索引位上的数据也移除
        # 2）将合理的pks转换为 objs


        objs = []
        new_request_data = []
        for index, pk in enumerate (pks):
            try:
                # 将pk合理的对象数据保存下来
                book_obj = models.Account_normal.objects.get (id=pk)
                objs.append (book_obj)
                # 对应索引的数据也保存下来,并且加人审批人和审批时间
                spobj = request_data[index]
                spobj.update(approve_id=request.user.id)
                spobj.update(approvetime=datetime.datetime.now())
                new_request_data.append (spobj)
            except:
                # 重点：反面教程 - pk对应的数据有误，将对应索引的data中request_data中移除
                # 在for循环中不要使用删除
                # index = pks.index(pk)
                # request_data.pop(index)
                continue
        # 生成一个serializer对象
        try:
            book_ser = serializers.normallistSerializer (instance=objs, data=new_request_data, partial=True, many=True)
            book_ser.is_valid (raise_exception=True)
            book_objs = book_ser.save ( )
            return Response ({
                'status': 200,
                'msg': 'ok',
                'results': serializers.normallistSerializer (book_objs, many=True).data
            })
        except Exception as ex :
            return Response ({
                'status': 501,
                'msg': 'err',
                'results': serializers.normallistSerializer (book_objs, many=True).data
            })




#查询视图
class Account_viewViewSet(viewsets.ModelViewSet):
    queryset = models.Account_view.objects.all()
    serializer_class = Account_viewSerializer
    pagination_class = MyPageNumberPagination
    filter_class = Account_view_FilterSet
    permission_classes = [IsOwnerOrReadOnlyForAccountView, ]



#附件
class attachmentViewSet(viewsets.ModelViewSet):
    queryset = models.attachment.objects.all()
    serializer_class = attachmentSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    # pagination_class = MyPageNumberPagination
    #删除的同时把存储的文件也删除了
    def perform_destroy(self, instance):
        instance.file.delete (save=False)
        instance.delete ( )

#合同信息
class Contract_infoViewSet(viewsets.ModelViewSet):
    queryset = models.Contract_info.objects.all()
    serializer_class = Contract_infoSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = MyPageNumberPagination
    filter_class = Contract_info_FilterSet

#合同财务计划
class Contract_planViewSet(viewsets.ModelViewSet):
    queryset = models.Contract_plan.objects.all()
    serializer_class = Contract_planSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_class = Cotract_plan_FilerSet
    # pagination_class = MyPageNumberPagination
