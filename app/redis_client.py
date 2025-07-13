import redis
from flask import current_app

redis_client = redis.StrictRedis.from_url("redis://localhost:6379/0", decode_responses=True)