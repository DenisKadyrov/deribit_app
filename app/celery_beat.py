from celery.schedules import crontab

from app.celery_app import celery_app

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.fetch_prices.fetch_and_store_prices",
        "schedule": crontab(minute="*"),
    }
}
