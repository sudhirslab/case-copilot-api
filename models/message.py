from datetime import datetime
from typing import Optional
from pydantic import BaseModel


"""
Message model
This model represents a message in the system.

Attributes:
    message_id (int): The unique identifier for the message.
    case_id (int): The unique identifier for the case.
    sender_id (int): The unique identifier for the sender of the message.
    content (str): The content of the message.
    created_at (datetime): The date and time the message was created.
    attachment (dict | None): The attachment of the message.
"""

class Message(BaseModel):
    message_id: int
    case_id: int
    sender_id: int
    content: str
    created_at: datetime = datetime.now()
    attachment: Optional[dict] = None

    
    @staticmethod
    def validate(data: dict, stores: dict, case_id: int):
        sender_id = data.get("sender_id")
        content = data.get("content")

        users = stores.get("users", [])
        cases = stores.get("cases", [])

        if not sender_id or not content:
            raise ValueError("sender_id and content are required")
        if not content.strip():
            raise ValueError("Message content cannot be empty")

        existing_case = next((c for c in cases if c.case_id == int(case_id) and c.status == "open"), None)
        if not existing_case:
            raise ValueError("Case not found")

        sender_user = next((u for u in users if u.user_id == int(sender_id)), None)
        if not sender_user:
            raise ValueError("Sender user not found")

        if sender_user.type == "user" and existing_case.owner_id != sender_user.user_id:
            raise ValueError("A regular user can only message their own case.")

        if sender_user.type not in {"user", "staff", "AI"}:
            raise ValueError("Unknown or unauthorized user type")

    @classmethod
    def create(cls, data: dict, stores: dict):
        cls.validate(data, stores, data["case_id"])
        return cls(
            message_id=data["message_id"],
            case_id=int(data["case_id"]),
            sender_id=int(data["sender_id"]),
            content=data["content"].strip(),
            attachment=data.get("attachment"),
        )
