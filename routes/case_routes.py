from fastapi import APIRouter, HTTPException
from models.case import Case
from data import case_store

router = APIRouter()


"""
Route: /cases
API to Create a new case

Method: POST
Args:
    owner_id (int): The unique identifier for the owner of the case.
    issue_description (str): The description of the issue.
"""
@router.post("/", response_model=Case)
def create_case(owner_id: int, issue_description: str):
    if not owner_id or not issue_description:
        raise HTTPException(status_code=400, detail="Missing required fields")

    new_case = Case(case_id=len(case_store.cases) + 1, owner_id=owner_id, issue_description=issue_description)
    case_store.cases.append(new_case)
    return new_case


"""
Route: /cases/{case_id}/close
API to close a case

Method: PUT
Args:
    case_id (int): The unique identifier for the case.
"""
@router.put("/{case_id}/close", response_model=Case)
def close_case(case_id: int):
    existing_case = next((c for c in case_store.cases if c.case_id == case_id), None)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")
    existing_case.status = "closed"
    return existing_case


"""
Route: /cases/{case_id}/reopen
API to reopen a case

Method: PUT
Args:
    case_id (int): The unique identifier for the case.
"""
@router.put("/{case_id}/reopen", response_model=Case)
def reopen_case(case_id: int):
    existing_case = next((c for c in case_store.cases if c.case_id == case_id), None)
    if not existing_case:
        raise HTTPException(status_code=404, detail="Case not found")
    if existing_case.status == "open":
        raise HTTPException(status_code=400, detail="Case is already open")
    existing_case.status = "open"
    return existing_case



"""
Route: /cases/user/{user_id}
API to get all cases for a user

Method: GET
Args:
    user_id (int): The unique identifier for the user.
"""
@router.get("/user/{user_id}", response_model=list[Case])
def get_user_cases(user_id: int):
    filtered_cases = [c for c in case_store.cases if c.owner_id == user_id and c.status == "open"]
    if not filtered_cases:
        raise HTTPException(status_code=404, detail="No cases found for this user")
    return filtered_cases
