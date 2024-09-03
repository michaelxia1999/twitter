from app.settings import REDIS_PWD
from redis.asyncio import StrictRedis

redis = StrictRedis(password=REDIS_PWD, decode_responses=True)