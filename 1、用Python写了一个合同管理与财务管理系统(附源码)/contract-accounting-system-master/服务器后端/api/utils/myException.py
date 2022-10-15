from rest_framework.response import Response
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # 先调用DRF默认的 exception_handler 方法, 对异常进行处理，
    # 如果处理成功，会返回一个`Response`类型的对象
    response = exception_handler(exc, context)

    if response is None:
        # 项目出错了，但DRF框架对出错的异常没有处理,
        # 可以在此处对异常进行统一处理，比如：保存出错信息到日志文件
        view = context['view']      # 出错的视图
        error = '服务器内部错误, %s' % exc
        print(context)
        print('111111111%s: %s' % (view, error))
        #如果是因为数据库外键关键出错，提示550
        if 'through a protected foreign' in error:
            return Response({'detail': error}, status=550)
        return Response({'detail': error}, status=500)

    return response
