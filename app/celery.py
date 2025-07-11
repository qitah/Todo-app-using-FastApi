from datetime import datetime
from celery import Celery

from app.db.session import get_db
from app.models.todos_model import Task

celery_app = Celery('app', 
                broker='redis://redis:6379/0',
                backend='redis://redis:6379/0'

)

celery_app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'app.celery.update_expired_task',
        'schedule': 30,  # every 30 seconds
    }
}

@celery_app.task
def update_expired_task():
    db = next(get_db())
    db.query(Task).filter(Task.is_expired == False, Task.due_date < datetime.now()).update({Task.is_expired: True}, synchronize_session=False)
    db.commit()
    db.close()

