#!/usr/bin/env python3

# Dependencies
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, root_validator

# user.py
# Author: Nicolas Delgado


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class UserConfig(BaseModel):
    language: str = "es"


class User(BaseModel):
    id: str
    is_active: bool = True
    role: Optional[UserRole]
    name: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    config: UserConfig = UserConfig()

    class Config:
        validate_assignment = True

    @root_validator
    def updated_at_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values
