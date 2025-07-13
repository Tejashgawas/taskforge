from flask import Blueprint,request
from .. import db
from ..models import User
from ..redis_client import redis_client
from ..utils import success, error
import uuid

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/login",methods = ["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    session_id = str(uuid.uuid4())

    user = User.query.filter_by(email = email).first()

    if not user or user.password != password:
        return error("invalid Credential")

    session_key = f"session:{session_id}"
    redis_client.hset(session_key,"logged_in", 1)
    redis_client.hset(session_key,"email",email)

    redis_client.expire(session_key,120)

    return success("Login successful",{"session_id":session_id})
    
@auth_bp.route("/me", methods=["GET"])
def get_profile():
    session_id = request.args.get("session_id")
    if not session_id:
        return error("Session ID missing", 400)

    session_key = f"session:{session_id}"
    logged_in = redis_client.hget(session_key, "logged_in")
    email = redis_client.hget(session_key, "email")

    if logged_in != "1":
        return error("Session expired", 401)

    return success("Session valid", {"email": email})

@auth_bp.route("/logout", methods=["GET"])
def logout():
    session_id = request.args.get("session_id")
    redis_client.delete(f"session:{session_id}")
    return success("Logged out")

