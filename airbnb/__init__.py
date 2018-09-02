from celery import Celery

redis = "redis://localhost:6379/0"
app = Celery("airbnb", broker=redis, backend=redis,
             include=['airbnb.tasks'])