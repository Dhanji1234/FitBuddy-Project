from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    weight: float  # Changed from int to float for more accurate weight representation
    goal: str
    intensity: str