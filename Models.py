from pydantic import BaseModel

class QueryModel(BaseModel):
    user_role: str
    query: str