# -*- copyright -*-

# Dependencies
# from firestore.firestore_connection import Firestore
from models.user import User
from serializers.user_serializers import GetUserByIdSerializer

# firestore_controller.py
# Author: Nicolas Delgado


class FirestoreController:
    def get_user_by_id(self, payload: GetUserByIdSerializer) -> User:
        # perorm query
        # response = Firestore().fs_client.collection().document().get()
        data = {
            "id": payload.user_id,
            "is_active": True,
            "role": "admin",
            "name": "test",
            "lastname": "user",
        }
        return User(**data)
