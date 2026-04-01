from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.market_routes import router as market_router
from app.routes.product_routes import router as product_router
from app.routes.seller_orders import router as orders_router
from app.routes.internal_product_routes import router as internal_products_router
import app.models 

app = FastAPI(title="Seller Backend Unified")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router)
app.include_router(product_router)
app.include_router(orders_router)
app.include_router(internal_products_router)