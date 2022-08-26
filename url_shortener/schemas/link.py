from datetime import datetime

from pydantic import BaseModel


class LinkInfo(BaseModel):
    id: int
    url: str
    created_at: datetime
