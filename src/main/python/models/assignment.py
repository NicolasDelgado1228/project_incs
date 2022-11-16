#!/usr/bin/env python3

# Dependencies
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel

# activity.py
# Author: Nicolas Delgado


class State(str, Enum):
    started = "started"
    finished = "finished"
    unstarted = "unstarted"


class Answer(BaseModel):
    id: str = str(uuid4())
    created_at: datetime = datetime.now()
    selected_image: str


class Assignment(BaseModel):
    id: str = str(uuid4())
    activity_id: str
    assigned_to: str
    assigned_by: str
    state: Optional[State]
    assigned_at: datetime = datetime.now()
    answers: Optional[List[Answer]] = []
