from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any, List, Dict

T = TypeVar("T")


class ApiError(BaseModel):
    code: str
    message: str
    meta: Dict[str, Any] = {}


class ApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    errors: List[ApiError] = []
    meta: Dict[str, Any] = {}

    class Config:
        from_attributes = True