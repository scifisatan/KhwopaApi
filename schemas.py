from typing import Literal
from enum import Enum

from pydantic import BaseModel, Field

class UserLoginSchema(BaseModel):
    username: str = Field(min_length=12, max_length=12)
    password: str = Field(min_length=10, max_length=10)


class ExamMarks(str, Enum):
    ASSESSMENT = "assessmentMarks"
    INTERNAL = "internalMarks"