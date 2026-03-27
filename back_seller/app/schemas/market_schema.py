from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

# Response GET /api/markets/my
class MarketResponse(BaseModel):

    marketId: UUID
    marketName: str
    description: Optional[str]
    createdAt: datetime

    class Config:
        from_attributes = True
# PATCH /api/markets/my
class MarketUpdate(BaseModel):

    marketName: str
    description: Optional[str]