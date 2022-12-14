# Dependenciess
from firestore.firestore_controller import FirestoreController
from flask import abort
from models.user import User
from serializers.user_serializers import SendInvitationSerializer
from utils.decorators import use_headers

# user_routes.py
# Author: Nicolas Delgado


@use_headers
def get_user_by_id_route(request, headers):
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "GET":
        payload = str(request.args.get("user_id"))
        user = FirestoreController().get_user_by_id(payload)
    else:
        return abort(400)

    return ({"users": user}, 200, headers)


@use_headers
def get_user_by_email_route(request, headers):
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "GET":
        payload = str(request.args.get("email"))
        user = FirestoreController().get_user_by_email(payload)
    else:
        return abort(400)

    return ({"user": user}, 200, headers)


@use_headers(allowed_methods=["POST"])
def invite_patient_route(request, headers):
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "POST":
        payload = SendInvitationSerializer(**request.args)
        email_data = FirestoreController().invite_patient(payload.dict())
    else:
        return abort(400)

    return ({"data": email_data}, 200, headers)


@use_headers(allowed_methods=["POST"])
def create_user_route(request, headers):
    """Create User"""
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        return ("", 200, headers)

    data = request.get_json()
    if data:
        payload = User(**data)
        user_new = FirestoreController().create_user(payload)
        return {"new_user": user_new}, 200, headers
    return abort(400)


@use_headers
def get_all_users_route(request, headers):
    """GET all users endpoint route"""
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "GET":
        users = FirestoreController().get_all_users()
    else:
        return abort(400)

    return ({"users": users}, 200, headers)
