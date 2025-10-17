from typing import List, Optional,Any
from pydantic import BaseModel
class Attachment(BaseModel):
    name: str
    url: str

class TaskRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: Any
    evaluation_url: str
    attachments: Optional[List[Attachment]] = None

class FileContext(BaseModel):
    file_name: str
    file_content: str
