from fastapi import APIRouter, HTTPException
from models.case import Case
from data import case_store

router = APIRouter()

@router.post("/", response_model=Case)
def create_case(owner_id: int, issue_description: str):
    if not owner_id or not issue_description:
        raise HTTPException(status_code=400, detail="Missing required fields")

    new_case = Case(case_id=len(case_store.cases) + 1, owner_id=owner_id, issue_description=issue_description)
    case_store.cases.append(new_case)
    return new_case

@router.put("/{case_id}/close", response_model=Case)
def close_case(case_id: int):
    existing_case = next((c for c in case_store.cases if c.case_id == case_id), None)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")
    existing_case.status = "closed"
    return existing_case

@router.put("/{case_id}/reopen", response_model=Case)
def reopen_case(case_id: int):
    existing_case = next((c for c in case_store.cases if c.case_id == case_id), None)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")
    if existing_case.status == "open":
        raise HTTPException(status_code=400, detail="Case is already open")
    existing_case.status = "open"
    return existing_case

