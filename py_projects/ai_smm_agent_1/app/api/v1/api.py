from fastapi import APIRouter

from app.api.v1.endpoints import products, content, social, analytics

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(social.router, prefix="/social", tags=["social"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
