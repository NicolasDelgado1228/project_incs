# -*- copyright -*-

# Dependencies
import os

import firebase_admin
from firebase_admin import credentials, firestore, storage

# firestore_connection.py
# Author: Nicolas Delgado
# Description: firestore singleton connection class


class Firestore:
    def __init__(self):
        self.storage_path = os.environ.get(
            "storage_path", "atencion-conjunta.appspot.com"
        )
        self.cred = credentials.ApplicationDefault()

        # init app
        firebase_admin.initialize_app(self.cred)

        # clients
        self.fs_client = firestore.client()
        self.fs_bucket = storage.bucket(self.storage_path)
