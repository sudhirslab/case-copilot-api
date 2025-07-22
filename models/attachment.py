from pydantic import BaseModel

"""
Attachment model
This model represents an attachment in the system.

Attributes:
    attachment_id (int): The unique identifier for the attachment.
    message_id (int): The unique identifier for the message.
    file_name (str): The name of the file.
    file_url (str): The URL of the file.
    thumbnail_url (str | None): The URL of the thumbnail.
"""

class Attachment(BaseModel):
    attachment_id: int
    message_id: int
    file_name: str
    file_url: str
    thumbnail_url: str | None = None

    @staticmethod
    def validate(file_name: str, file_url: str):
        if not file_name or not file_url:
            raise ValueError("file_name and file_url are required")

    @classmethod
    def create(cls, data: dict):
        cls.validate(data.get("file_name"), data.get("file_url"))
        return cls(
            attachment_id=data["attachment_id"],
            message_id=int(data["message_id"]),
            file_name=data["file_name"],
            file_url=data["file_url"],
        )
