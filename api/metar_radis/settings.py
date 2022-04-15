import redis
from django.conf import settings


redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)
METAR_ENDPOINT = "http://tgftp.nws.noaa.gov/data/observations/metar"