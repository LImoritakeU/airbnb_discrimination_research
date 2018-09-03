from celery import Celery

from conf import redis_url

redis = redis_url
app = Celery("airbnb", broker=redis, backend=redis,
             include=['airbnb.tasks'])