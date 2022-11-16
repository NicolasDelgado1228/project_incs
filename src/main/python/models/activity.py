#!/usr/bin/env python3

# Dependencies
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel

# activity.py
# Author: Nicolas Delgado


class Card(BaseModel):
    id: str = str(uuid4())
    created_at: datetime = datetime.now()
    images: List[str] = []
    description: Optional[str]
    correct_image: Optional[str]


class Activity(BaseModel):
    id: str = str(uuid4())
    owner: str
    created_at: datetime = datetime.now()
    description: Optional[str]
