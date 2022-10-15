
# 自定义状态码
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class HttpCode(object):
    # 正常登陆
    ok = 200
    #未注册
    notregister = 300
    # 参数错误
    paramserror = 400
    # 权限错误
    unauth = 401
    # 方法错误
    methoderror = 405

    # 服务器内部错误
    servererror = 500


# 定义统一的 json 字符串返回格式
def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}
    # isinstance(object对象, 类型):判断是否数据xx类型
    if kwargs and isinstance (kwargs, dict) and kwargs.keys ( ):
        json_dict.update (kwargs)
    response = JsonResponse (json_dict,json_dumps_params={'ensure_ascii':False},status=code)

    return response


def ok():
    return result ( )


# 参数错误
def params_error(message="", data=None):
    return result (code=HttpCode.paramserror, message=message, data=data)


# 权限错误
def unauth(message="", data=None):
    return result (code=HttpCode.unauth, message=message, data=data)


# 方法错误
def method_error(message="", data=None):
    return result (code=HttpCode.methoderror, message=message, data=data)


# 服务器内部错误
def server_error(message="", data=None):
    return result (code=HttpCode.servererror, message=message, data=data)
