from flask import Blueprint,request
from ..models import Article
from ..import db
from ..redis_client import redis_client
from ..utils import success,error
import json

cache_bp = Blueprint("cache",__name__)

@cache_bp.route("/articles/<int:article_id>",methods = ["GET"])
def get_article(article_id):
    key = f"article:{article_id}"

    cached = redis_client.get(key)

    if cached:
        return success("From redis",json.loads(cached))
    
    article = Article.query.get(article_id)

    if not article:
        return error("Artical not present")
    
    article_data = {
        "id" : article.id,
        "title" : article.title,
        "content": article.content,
        "created_at": article.created_at.strftime('%Y-%m-%d %H:%M:%S')

    }

    redis_client.set(key,json.dumps(article_data),ex=30)

    return success("From DB",article_data)

@cache_bp.route("/articles/<int:article_id>/clear-cache", methods=["POST"])
def clear_article_cache(article_id):
    key = f"article:{article_id}"
    redis_client.delete(key)
    return success(f"Cache for article {article_id} cleared")

@cache_bp.route("/articles/<int:article_id>/ttl", methods=["GET"])
def get_article_ttl(article_id):
    key = f"article:{article_id}"
    ttl = redis_client.ttl(key)
    if ttl == -2:
        return error("No cache found for this article")
    return success(f"Cache TTL: {ttl} seconds", data={"ttl": ttl})

