# 实例化celery对象
from celery import Celery
from config import CeleryConfig

celery_task = Celery('fr_celery')
celery_task.config_from_object(CeleryConfig)


@celery_task.task
def task_def():
    print(444)



# 启动命令：
# win11:celery_fr --app=celery_app:celery_task worker  -l info -P eventlet
# win10:celery  --app=app:celery_task worker --pool=solo --loglevel=info
# linux:sudo /home/admin/.virtualenvs/flexibleRates/bin/celery  --app=apps.celery_fr.celery_app:celery_task worker --pool=solo --loglevel=info -E
