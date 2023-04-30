from fastapi import APIRouter, Depends

from src.auth.auth import current_user
from src.tasks.tasks import send_email


router = APIRouter(prefix="/report")


@router.get("/mail")
def get_report_to_email(user=Depends(current_user)):
    send_email.delay(user.username, user.email)
    return {
        "status": "OK",
        "data": None,
        "detail": "Message sent"
    }
