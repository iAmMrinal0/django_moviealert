from celery.decorators import periodic_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from moviealert.search import search_movie

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour="*", minute="0", day_of_week="*")))
def search_movie_task():
    """search a movie and print if found successfully"""
    logger.info("Finding a movie")
    return search_movie()
