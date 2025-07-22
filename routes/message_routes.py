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

class AttachmentData(BaseModel):
    file_name: str
    file_url: str

class MessageRequest(BaseModel):
    sender_id: int
    content: str
    attachment: Optional[AttachmentData] = None

class EditMessageRequest(BaseModel):
    sender_id: int
    content: str

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

@router.get("/{case_id}/messages")
def get_messages(case_id: int):
    existing_case = next((c for c in cases if c.case_id == case_id and c.status == "open"), None)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")
    filtered = [m for m in messages if m.case_id == case_id]
    return filtered

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
