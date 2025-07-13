from flask import Blueprint,jsonify
from ..redis_client import redis_client
from .otp import otp_bp
from .limiter import limiter_bp
from .cache import cache_bp
from .auth import auth_bp

def init_routes(app):
    base = Blueprint("base",__name__)

    @base.route("/ping-redis")
    def ping_redis():
        try:
            pong = redis_client.ping()
            return jsonify({"redis": "connected" if pong else "failed"})
        except Exception as e:
            return jsonify({"error": str(e)}),500
        
    app.register_blueprint(base)
    app.register_blueprint(otp_bp)
    app.register_blueprint(limiter_bp)
    app.register_blueprint(cache_bp)
    app.register_blueprint(auth_bp)