# Dependenciess
from firestore.firestore_controller import FirestoreController
from flask import abort
from utils.decorators import use_headers

# user_routes.py
# Author: Nicolas Delgado


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
