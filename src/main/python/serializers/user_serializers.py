#!/usr/bin/env python3

# Dependencies
from pydantic import BaseModel

# user_serializers.py
# Author: Nicolas Delgado


class GetUserByIdSerializer(BaseModel):
    user_id: str


class SendInvitationSerializer(BaseModel):
    email: str
    name: str
    lastname: str
