from pydantic import BaseModel
from app.model.contants import Country

class NameRequest(BaseModel):
    full_name: str
    country: str

class NameResponse(BaseModel):
    first_name: str
    last_name: str
    chance: float

