# Dependenciess
from firestore.firestore_controller import FirestoreController
from flask import abort
from utils.decorators import use_headers
from models.activity import Activity

# user_routes.py
# Author: Nicolas Delgado


@use_headers
def get_activity_by_id_route(request, headers):
    """GET all users endpoint route"""
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "GET":
        activity_id = str(request.args.get("id"))
        payload = {"id": activity_id}
        activities = FirestoreController().generic_search(payload, "ACTIVITIES")
    else:
        return abort(400)

    return ({"activities": activities}, 200, headers)


@use_headers
def get_activity_by_owner_route(request, headers):
    """GET all users endpoint route"""
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "GET":
        owner_id = str(request.args.get("owner_id"))
        payload = {"owner": owner_id}
        activities = FirestoreController().generic_search(payload, "ACTIVITIES")
    else:
        return abort(400)

    return ({"activities": activities}, 200, headers)


@use_headers(allowed_methods=["POST"])
def create_activity_route(request, headers):
    """Create User"""
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        return ("", 200, headers)

    data = request.get_json()
    if data:
        payload = Activity(**data)
        new_activity = FirestoreController().create_activity(payload)
        return {"new_activity": new_activity}, 200, headers
    return abort(400)
