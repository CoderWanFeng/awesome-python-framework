import hashlib

from django.contrib.auth.backends import ModelBackend, AllowAllUsersModelBackend
from django.db.models import Q
from rest_framework import exceptions, permissions
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import BasePermission
from django.db import models
from api import models
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.parsers import FormParser

from api.models import UserInfo


def get_authorization_header(request):
    """
     Return request's 'Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth

#权限认证
class ApiPermission1(BasePermission):
    message = "需要2级权限"
    def has_permission(self,request,view):
        if request.user.user_type !=2: #判断权限类型
            return False
        return True
class ApiPermission2(object):
    def has_permission(self,request,view):
        if request.user.user_type ==1: #判断权限类型
            return True
        return False

#普通用户只能改自己的密码
class IsAdminOrReadOnlyForUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # 带具体id检测
        # 管理员放行
        if request.user.user_type == 2:
            return True
        #安全方法放行
        if request.method in permissions.SAFE_METHODS:
            return obj == request.user
        #如果PATCH方法是改密码并且是自己的密码
        if request.method in ('PATCH'):
            return  ('password' in request.data) & (obj == request.user)

        return False
    def has_permission(self, request, view):#全局检测 所有url  这个方法在先
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print ("开始检查权限整体")
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.user_type == 2:
            #print ("这是个管理员，让他去")
            return True
        #Put delete path 操作
        if request.method not in permissions.SAFE_METHODS:
            url = ("/api/users/")
            request = request._request
            #如果是单个对象操作，放行
            if request.path not in url:
                return True
            else:
                return False
        return False
#不是管理员只有只读权限
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # 带具体id检测
        #安全方法放行
        if request.method in permissions.SAFE_METHODS:
            return True
        #管理员放行
        if request.user.user_type == 2:
            return True
        return False
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.user_type == 2
        )
#只有管理员和对象本人才可以修改删除，否则只能读取
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            print("安全方法")
            return True
        if request.user.user_type == 2:
            return True
        # Instance must have an attribute named `owner`.
        # return obj.user == request.user 这里的request.user是认证时候给过来的返回值
        return obj == request.user

#只有管理员和对象本人才可以修改删除，否则只能读取，而且一但状态变成已报销后不能做DML操作
class IsOwnerOrReadOnlyForAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):#带具体id检测
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # print("开始检查对象权限")
        if request.method in permissions.SAFE_METHODS:
            # print ("安全方法")
            return True
        if request.user.user_type == 2:
            # print ("这是个管理员，让他去")
            return True
        # Instance must have an attribute named `owner`.
        # 判断出差记录的报销人
        if request.method in ('DELETE','PUT','PATCH'):
            # print ("这是一个'DELETE','PUT'请求",'PATCH')
            # print('完成状态是'+obj.finish_flag)
            if obj.finish_flag == '0':
                return obj.expense_name == request.user
            else:
                return False
        print ("最后的判断")
        return obj.expense_name == request.user

    def has_permission(self, request, view):#全局检测 所有url
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print ("开始检查权限整体")
        if request.user.user_type == 2:
            print ("这是个管理员，让他去")
            return True
        if request.method  in ("POST",):
            return True
        #Put delete path 操作
        if request.method not in permissions.SAFE_METHODS:
            url = ("/api/Account_normals/","/api/Account_projects/",)
            request = request._request
            #如果是单个对象操作，放行
            if request.path not in url:
                return True
            else:
                return False
        # except :
        #     return False
        # if request.method not in permissions.SAFE_METHODS:
        #     request.user

        return True
# 默认请求验证类
class ApiAuthentication(TokenAuthentication):
    def authenticate(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败！')
        #rest framework内部会用到元组内的两个字段段，request.user request.auth
        return (token_obj.user,token_obj)
    def authenticate_header(self,val):
        pass

class IsOwnerOrReadOnlyForAccountView(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print("开始检查对象权限")
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if request.user.user_type == 2:
            return True
        # Instance must have an attribute named `owner`.
        # 判断出差记录的报销人
        # if request.method in ('GET'):
            # if obj.finish_flag == '0':
            #     return obj.expense_name == request.user
            # else:
            #     return False
        print(obj.expense_name == request.user)
        return obj.expense_name == request.user
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # print ("ajajajajajjajajajajajjajaj")
        return True

# 默认请求验证类

class CusertomBackend(AllowAllUsersModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get (username=username)

            if user.password == password:
                return user
        except Exception as e:
            print (e)
            return None
          # try:
            #     id = request.data['id']
            #     obj = models.UserToken.objects.filter(id=id).first()
            #     if obj['expense_name'] == request.user.id:
