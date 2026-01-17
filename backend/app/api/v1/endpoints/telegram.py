
from fastapi import APIRouter, Header, HTTPException
from app.core.config import settings
from app.services.telegram_service import handle_command

router = APIRouter()

@router.post("/telegram/webhook")
async def telegram_webhook(
    payload: dict,
    x_telegram_bot_api_secret_token: str = Header(...)
):
    if x_telegram_bot_api_secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    await handle_command(payload)
    return {"ok": True}
