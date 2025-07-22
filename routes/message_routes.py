from fastapi import APIRouter, HTTPException
from models.message import Message
from data.user_store import users
from data.case_store import cases
from data.message_store import messages
from data.attachment_store import attachments
from utilities.thumbnail_generator import generate_thumbnail
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


"""
AttachmentData model

Attributes:
    file_name (str): The name of the file.
    file_url (str): The URL of the file.
"""
class AttachmentData(BaseModel):
    file_name: str
    file_url: str



"""
MessageRequest model

Attributes:
    sender_id (int): The unique identifier for the sender of the message.   
    content (str): The content of the message.
    attachment (Optional[AttachmentData]): The attachment of the message.
"""
class MessageRequest(BaseModel):
    sender_id: int
    content: str
    attachment: Optional[AttachmentData] = None



"""
EditMessageRequest model

Attributes:
    sender_id (int): The unique identifier for the sender of the message.
    content (str): The content of the message.
"""
class EditMessageRequest(BaseModel):
    sender_id: int
    content: str



"""
Route: /{case_id}/messages
API to create a new message

Method: POST
Args:
    case_id (int): The unique identifier for the case.
    body (MessageRequest): The request body.
"""
@router.post("/{case_id}/messages")
def create_message(case_id: int, body: MessageRequest):
    try:
        new_message = Message.create({
            "message_id": len(messages) + 1,
            "case_id": case_id,
            "sender_id": body.sender_id,
            "content": body.content,
            "attachment": body.attachment.dict() if body.attachment else None,
        }, { "users": users, "cases": cases })
        messages.append(new_message)

        if body.attachment:
            new_attachment = {
                "attachment_id": len(attachments) + 1,
                "message_id": new_message.message_id,
                "file_name": body.attachment.file_name,
                "file_url": body.attachment.file_url,
            }
            try:
                thumbnail_path = f"public/thumbnails/thumb_{body.attachment.file_name}"
                generate_thumbnail(body.attachment.file_url, thumbnail_path)
                new_attachment["thumbnail_url"] = thumbnail_path
            except Exception:
                new_attachment["thumbnail_url"] = None
            attachments.append(new_attachment)

        return new_message
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



"""
Route: /{case_id}/messages
API to get all messages for a case

Method: GET
Args:
    case_id (int): The unique identifier for the case.
"""
@router.get("/{case_id}/messages")
def get_messages(case_id: int):
    existing_case = next((c for c in cases if c.case_id == case_id and c.status == "open"), None)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")
    filtered = [m for m in messages if m.case_id == case_id]
    return filtered



"""
Route: /{case_id}/messages/{message_id}/attachments
API to get all attachments for a message

Method: GET
Args:
    case_id (int): The unique identifier for the case.
    message_id (int): The unique identifier for the message.
"""
@router.get("/{case_id}/messages/{message_id}/attachments")
def get_message_attachments(case_id: int, message_id: int):
    existing_case = next((c for c in cases if c.case_id == case_id and c.status == "open"), None)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")
    existing_message = next((m for m in messages if m.message_id == message_id), None)
    if not existing_message:
        raise HTTPException(status_code=404, detail="Message not found")
    filtered_attachments = [a for a in attachments if a["message_id"] == message_id]
    return filtered_attachments



"""
Route: /{case_id}/messages/{message_id}/edit
API to edit a message

Method: POST
Args:
    case_id (int): The unique identifier for the case.
    message_id (int): The unique identifier for the message.
    body (EditMessageRequest): The request body.
"""
@router.post("/{case_id}/messages/{message_id}/edit")
def edit_message(case_id: int, message_id: int, body: EditMessageRequest):
    existing_case = next((c for c in cases if c.case_id == case_id and c.status == "open"), None)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")

    existing_message = next((m for m in messages if m.message_id == message_id), None)
    if not existing_message:
        raise HTTPException(status_code=404, detail="Message not found")

    if body.sender_id != existing_message.sender_id:
        raise HTTPException(status_code=403, detail="Only the original sender can edit the message")

    if not body.content.strip():
        raise HTTPException(status_code=400, detail="Message content cannot be empty")

    existing_message.content = body.content.strip()
    return existing_message
