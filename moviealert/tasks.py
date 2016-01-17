from celery.decorators import task
from celery.utils.log import get_task_logger

from moviealert.search import search_movie

logger = get_task_logger(__name__)


@task(name="search_movie_task")
def search_movie_task():
    """search a movie and print if found successfully"""
    logger.info("Finding a movie")
    return search_movie()
