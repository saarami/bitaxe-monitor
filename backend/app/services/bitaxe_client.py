
from app.core.http_client import get_json
from app.core.config import settings
import time

async def fetch_system_info():
    start = time.time()
    data = await get_json(f"{settings.BITAXE_BASE_URL}/api/system/info")
    data["_response_time_ms"] = (time.time() - start) * 1000
    return data
