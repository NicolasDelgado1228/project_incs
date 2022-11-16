# -*- copyright -*-

# Dependencies
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP
from typing import List
from uuid import uuid4

from firestore.firestore_connection import Firestore
from models.activity import Activity
from models.assignment import Assignment, State
from models.user import User
from utils.email_templates import EmailTemplates

# firestore_controller.py
# Author: Nicolas Delgado


class FirestoreController:
    def get_user_by_id(self, user_id: str) -> dict:
        response = Firestore().fs_client.collection("USERS").document(user_id).get()
        if response.exists:
            return response.to_dict()

        return {}

    def get_user_by_email(self, email: str) -> dict:
        response = [
            document.to_dict()
            for document in Firestore()
            .fs_client.collection("USERS")
            .where("email", "==", email)
            .stream()
        ]
        if response:
            return response[0]

        return {}

    def generic_subupdate(self, payload) -> dict:
        doc = (
            Firestore()
            .fs_client.collection(payload["main_collection"])
            .document(payload["main_document"])
            .collection(payload["collection"])
            .document(payload["document"])
        )
        if doc.get().exists:
            print(f"[LOG] updating document {payload['document']}")
            doc.update(payload["data"])
        else:
            print("[LOG] Fail update. Doc not exist")
        return doc.get().to_dict()

    def generic_update(self, payload) -> dict:
        doc = (
            Firestore()
            .fs_client.collection(payload["collection"])
            .document(payload["document"])
        )
        payload["data"] = payload["data"]
        if doc.get().exists:
            doc.update(payload["data"])
        return doc.get().to_dict()

    def generic_subget(self, payload) -> object:
        return (
            Firestore()
            .fs_client.collection(payload["main_collection"])
            .document(payload["main_document"])
            .collection(payload["collection"])
            .document(payload["document"])
            .get()
            .to_dict()
        )

    def generic_get(self, payload) -> object:
        return (
            Firestore()
            .fs_client.collection(payload["collection"])
            .document(payload["document"])
            .get()
            .to_dict()
        )

    def generic_get_query_equal(self, payload) -> object:
        return [
            doc.to_dict()
            for doc in Firestore()
            .fs_client.collection(payload["collection"])
            .where(payload["query_param"], "==", payload["param"])
            .stream()
        ]

    def get_querysets(self, payload):
        or_keys = payload.pop("or_fields", "").split(",")
        or_fields = and_fields = {}

        for key in payload:
            if key in or_keys:
                or_fields = {**or_fields, key: payload[key]}
            else:
                and_fields = {**and_fields, key: payload[key]}

        return [{**and_fields, key: or_fields[key]} for key in or_fields]

    def generic_search(
        self, payload, collection, order_by=None, base=None
    ) -> List[object]:
        base = base if base else Firestore().fs_client.collection(collection)

        querysets = self.get_querysets(payload)

        # Return all if not payload provided
        response = {doc.id: doc.to_dict() for doc in base.stream()}

        if querysets:
            for queryset in querysets:
                query_base = base
                for key in queryset:
                    query_base = query_base.where(key, "==", queryset[key])

                response = {
                    **response,
                    **{doc.id: doc.to_dict() for doc in query_base.stream()},
                }
        elif payload:
            for key in payload:
                base = base.where(key, "==", payload[key])
            if order_by:
                base = base.order_by(order_by)
            response = {doc.id: doc.to_dict() for doc in base.stream()}

        return list(response.values())

    def generic_subsearch(
        self,
        payload,
        main_collection,
        main_document,
        collection,
        order_by=None,
        base=None,
    ):
        return self.generic_search(payload, collection, order_by=order_by, base=base)

    def generic_delete_document(self, payload) -> object:
        doc_ref = (
            Firestore()
            .fs_client.collection(payload["collection"])
            .document(payload["document"])
        )
        if doc_ref.get().exists:
            doc_ref.delete()
            print("[LOG] Document deleted successfully!")
            return True

        print("[LOG] El documento no existe!")

        return False

    def create_user(self, user: User) -> dict:
        user_dict = user.dict()
        user_dict["created_at"] = datetime.now()
        user_dict["id"] = str(uuid4())
        Firestore().fs_client.collection("USERS").document(str(user_dict["id"])).set(
            user_dict
        )
        return user_dict

    def create_activity(selef, activity: Activity) -> dict:
        activity_dict = activity.dict()
        activity_dict["created_at"] = datetime.now()

        Firestore().fs_client.collection("ACTIVITIES").document(
            str(activity_dict["id"])
        ).set(activity_dict)

        return activity_dict

    def create_assignment(selef, assignment: Assignment) -> dict:
        assignment_dict = assignment.dict()
        assignment_dict["assigned_at"] = datetime.now()
        assignment_dict["state"] = State.unstarted

        Firestore().fs_client.collection("ASSIGNMENTS").document(
            str(assignment_dict["id"])
        ).set(assignment_dict)

        return assignment_dict

    def create_card_activity(self, payload) -> dict:
        payload["id"] = str(uuid4())
        payload["created_at"] = datetime.now()

        Firestore().fs_client.collection("ACTIVITIES").document(
            str(payload["activity_id"])
        ).collection("CARDS").document(payload["id"]).set(payload)

        return payload

    def create_answer_assignment(self, payload) -> dict:
        payload["id"] = str(uuid4())
        payload["created_at"] = datetime.now()

        Firestore().fs_client.collection("ASSIGNMENTS").document(
            str(payload["assignment_id"])
        ).collection("ANSWERS").document(payload["id"]).set(payload)

        return payload

    def update_user(self, user: User) -> dict:
        user_ref = Firestore().fs_client.collection("USERS").document(user.id)
        if user_ref.get().exists:
            user_ref.update(user.dict())

    def send_email(self, data: dict) -> None:
        fromEmail = "noreply@piyion.com"
        toEmail = data["receiver_email"]

        message = MIMEMultipart()
        message["Subject"] = data["subject"]
        message["From"] = fromEmail
        message["To"] = toEmail
        rcpt = [fromEmail, toEmail]

        body = data["body"]
        textMessage = MIMEText(body, "html")
        message.attach(textMessage)

        connection = SMTP("piyion.com", 465)
        connection.login(fromEmail, "Piyion2021")

        try:
            connection.sendmail(fromEmail, rcpt, message.as_string())
        finally:
            connection.close()

    def invite_patient(self, data: dict) -> dict:
        data["patient_name"] = f"{data['name']} {data['lastname']}"
        data["subject"] = f"¡Hola {data['patient_name']}, únete a NOMBRE PLATAFORMA"
        data["body"] = EmailTemplates.invitation_email.replace(
            "##PATIENT_NAME##", data["patient_name"]
        )
        data["receiver_email"] = data["email"]
        self.send_email(data)

        return data

    def get_all_users(self):
        users = [
            user.to_dict()
            for user in Firestore().fs_client.collection("USERS").stream()
        ]

        return users

    def get_all_activities(self):
        activities = [
            activity.to_dict()
            for activity in Firestore().fs_client.collection("ACTIVITIES").stream()
        ]

        return activities
