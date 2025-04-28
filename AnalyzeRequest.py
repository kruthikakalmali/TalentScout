
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    session_id: str