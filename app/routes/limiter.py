from flask import Blueprint,request
from ..redis_client import redis_client
from ..utils import success,error

limiter_bp = Blueprint("limiter",__name__)

@limiter_bp.route("/limited-endpoint",methods = ["GET"])
def limited_endpoint():
    ip = request.remote_addr
    key = f"rate:{ip}"
    limit = 5
    window = 60

    count = redis_client.incr(key)
    print(count)

    if redis_client.ttl(key) == -1:
        redis_client.expire(key, window)

    
    if count > 5:
        ttl = redis_client.ttl(key)
        wait_time = ttl if ttl > 0 else window
        return error(f"Rate limit exceeded,Try again in {wait_time}s",429)
    
    return success(f"allowed : {count}/5 request in current {window}")

