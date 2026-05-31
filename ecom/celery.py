import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings') # 'ecom' is name of main project for you

app = Celery('ecom')# 'ecom' is name of main project for you

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



# run celery comand [ celery -A ecom worker --loglevel=info -P eventlet -c 10 ]
