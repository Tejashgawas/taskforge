from flask import Blueprint,request,jsonify
from ..redis_client import redis_client
from ..utils import generate_otp,success,error

otp_bp = Blueprint("otp",__name__)

@otp_bp.route('/send-otp',methods = ["POST"])
def send_otp():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return error("Email is required")
    
    otp = generate_otp()
    key = f"otp:{email}"

    redis_client.set(key,otp,ex=60)
     # (✅ simulate sending via email - we'll just print it)
    print(f"🔐 OTP for {email}: {otp}")

    return success("OTP sent successfully",{"otp": otp})

@otp_bp.route("/verify-otp",methods = ["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    entered_otp = data.get("otp")

    if not email or not entered_otp:
        return error("email and otp is required")
    
    key = f"otp:{email}"

    stored_otp = redis_client.get(key)

    if stored_otp is None:
        return error("Otp is expired!")
    
    if entered_otp == stored_otp:
        redis_client.delete(key)
        return success("Otp verified")
    else:
        return error("otp is invalid")

