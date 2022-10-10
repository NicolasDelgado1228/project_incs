# Dependencies
import json

from firestore.firestore_controller import FirestoreController
from flask import abort
from serializers.user_serializers import GetUserByIdSerializer
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
        payload = GetUserByIdSerializer(**request.args)
        user = FirestoreController().get_user_by_id(payload)
        response = json.loads(user.json())
    else:
        return abort(400)

    return ({"users": response}, 200, headers)
