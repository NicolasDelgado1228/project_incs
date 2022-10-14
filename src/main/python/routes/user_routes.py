# Dependencies
import json

from firestore.firestore_controller import FirestoreController
from flask import abort
from models.user import User
from serializers.user_serializers import GetUserByIdSerializer, SendInvitationSerializer
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


def _get_user_by_id_route(request, headers):
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "GET":
        payload = GetUserByIdSerializer(**request.args)
        user = FirestoreController().get_user_by_id(payload)
        response = json.loads(user.json())
    else:
        return abort(400)

    return ({"users": response}, 200, headers)


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
