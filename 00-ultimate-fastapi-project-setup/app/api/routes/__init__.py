from api.routes.v1 import router as v1_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(v1_router)
