from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from app.models.order import OrderStatus


class CustomerOut(BaseModel):
    id: UUID
    full_name: str
    telegram: Optional[str]


class OrderOut(BaseModel):
    id: UUID
    order_number: str
    customer: CustomerOut
    delivery_address: Optional[str]
    total_amount: float
    items_count: int
    status: OrderStatus
    created_at: datetime


class StatisticsOut(BaseModel):
    total_orders: int
    total_revenue: float
    completed_orders: int
    processing_orders: int
    pending_orders: int


class OrderStatusUpdate(BaseModel):
    status: OrderStatus