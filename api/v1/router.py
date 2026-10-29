from fastapi import APIRouter

from api.v1.routes import job_ana

api_router = APIRouter()

api_router.include_router(job_ana.router)
# api_router.include_router(user.router)
# api_router.include_router(process.router)
# api_router.include_router(chat.router)