# Dependenciess
from firestore.firestore_controller import FirestoreController
from flask import abort
from utils.decorators import use_headers

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
        activity_id = str(request.args.get("activity_id"))
        payload = {"activity_id": activity_id}
        activities = FirestoreController().generic_search(payload, "ACTIVITIES")
    else:
        return abort(400)

    return ({"activities": activities}, 200, headers)
