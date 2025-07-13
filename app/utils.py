import random
from flask import jsonify

def generate_otp(length=4):
    return ''.join([str(random.randint(0,9))for _ in range(length)])

def success(message=None,data=None,status=200):
    response = {"success":True}
    if message:
        response["message"] = message
    if data:
        response["data"] = data
    
    return jsonify(response),status

def error(message="Something went wrong", status=400):
    return jsonify({"success": False, "message": message}), status
