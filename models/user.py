from pydantic import BaseModel

"""
User model
This model represents a user in the system.

Attributes:
    user_id (int): The unique identifier for the user.
    name (str): The name of the user.
    type (str): The type of user.

"""

class User(BaseModel):
    user_id: int
    name: str
    type: str
