from apps.product.models import Product
from celery import shared_task
from celery.schedules import crontab
from apps.users.services.utils import send_activation_code, send_notification_message
from config.celery import app
# app.conf.beat_schedule = {
#     # Executes every day at  12:30 pm.
#     'run-every-evening': {
#         'task': 'tasks.elast',
#         'schedule': crontab(hour=0, minute=1),
#         'args': (),
#     },
# }


@shared_task
def sent_notification_task(email):
    send_notification_message(email)

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Product.objects.count()


@shared_task
def rename_widget(widget_id, name):
    w = Product.objects.get(id=widget_id)
    w.name = name
    w.save()
