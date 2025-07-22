from datetime import datetime
from pydantic import BaseModel

"""
Case model
This model represents a case in the system.

Attributes:
    case_id (int): The unique identifier for the case.
    owner_id (int): The unique identifier for the owner of the case.
    issue_description (str): The description of the issue.
    status (str): The status of the case.
    created_at (datetime): The date and time the case was created.
"""

class Case(BaseModel):
    case_id: int
    owner_id: int
    issue_description: str
    status: str = "open"
    created_at: datetime = datetime.now()
