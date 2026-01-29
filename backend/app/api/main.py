from fastapi import APIRouter

from app.api.routes import cmd, users, login, activity_category, activity, daily_report, mood, sleep

api_router = APIRouter()
api_router.include_router(cmd.router)
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(activity_category.router)
api_router.include_router(activity.router)
api_router.include_router(daily_report.router)
api_router.include_router(mood.router)
api_router.include_router(sleep.router)
