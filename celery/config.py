from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CeleryConfig():
    # timezone = 'UTC'
    broker_url = 'redis://:Hx$hfcmsrx3@localhost:6379/4'  # 消息队列存放地址
    result_backend = 'redis://:Hx$hfcmsrx3@localhost:6379/5'  # celery_fr worker 执行结果返回存放地址
    # BROKER_URL = 'redis://localhost:6379/4'  # 消息队列存放地址
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/5'  # celery_fr worker 执行结果返回存放地址
    timezone = 'Asia/Shanghai'  # 时区
    task_acks_late = True  # 只有当worker执行完任务后，才会告诉MQ，消息被消费。
    CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
    task_ignore_result = False  # 忽略结果，不关心运行结果时可以关闭
    task_serializer = 'json'  # 任务序列化方式
    worker_disable_rate_limits = True  # 对任务消费的速率进行限制开关
    worker_prefetch_multiplier = 1  # worker预先获取任务数量
    worker_max_tasks_per_child = 30  # worker最大执行任务数，超过数量销毁，防止内存泄漏等问题
    task_create_missing_queues = True  # 队列不存在即创建
    broker_transport_options = {'visibility_timeout': 7 * 24 * 60 * 60, 'max_retries': 1}  # celery_fr worker超时自动重启时间
    worker_concurrency = 3  # celery_fr worker 最大并行数
