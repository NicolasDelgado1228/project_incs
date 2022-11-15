# Dependenciess
from firestore.firestore_controller import FirestoreController
from flask import abort

from models.assignment import Assignment
from utils.decorators import use_headers

# activity_routes.py
# Author: Nicolas Delgado


@use_headers
def get_all_assignments_by_assigned_to_route(request, headers):
    """GET get_all_assignments_by_assigned_to"""
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "GET":
        assigned_to = str(request.args.get("assigned_to"))
        payload = {"assigned_to": assigned_to}
        assignments = FirestoreController().generic_search(payload, "ASSIGNMENTS")
    else:
        return abort(400)

    return ({"assignments": assignments}, 200, headers)


@use_headers
def get_all_assignments_by_assigned_by_route(request, headers):
    """GET get_all_assignments_by_assigned_to"""
    request_method = request.method

    # Set CORS headers for the preflight request
    if request_method == "OPTIONS":
        return ("", 200, headers)

    if request_method == "GET":
        assigned_to = str(request.args.get("assigned_by"))
        payload = {"assigned_by": assigned_to}
        assignments = FirestoreController().generic_search(payload, "ASSIGNMENTS")
    else:
        return abort(400)

    return ({"assignments": assignments}, 200, headers)


@use_headers(allowed_methods=["POST"])
def create_assignment_route(request, headers):
    """Create Assignment"""
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        return ("", 200, headers)

    data = request.get_json()
    if data:
        payload = Assignment(**data)
        new_activity = FirestoreController().create_assignment(payload)
        return {"new_activity": new_activity}, 200, headers
    return abort(400)
