#!/usr/bin/env python3

# Dependencies
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

# activity.py
# Author: Nicolas Delgado


class Assignment(BaseModel):
    id: str
    assigned_to: str
    assigned_at: datetime = datetime.now()
    answers: Optional[List[str]]


class Activity(BaseModel):
    id: str
    owner: str
    assignments: Optional[List[Assignment]]
    created_at: datetime = datetime.now()
    images: Optional[List[str]]