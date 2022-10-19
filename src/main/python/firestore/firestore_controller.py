# -*- copyright -*-

# Dependencies
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP
from uuid import uuid4

from firestore.firestore_connection import Firestore
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

    def create_user(self, user: User) -> dict:
        user_dict = user.dict()
        user_dict["created_at"] = datetime.now()
        user_dict["id"] = str(uuid4())
        Firestore().fs_client.collection("USERS").document(str(user_dict["id"])).set(
            user_dict
        )
        return user_dict

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
