import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import httpx
from astrbot.api import AstrBotConfig
from astrbot.api import logger
from .qchttpx import QUICKHTTPX

class OCSTATUS:
    def __init__(self, config: AstrBotConfig):
        self.config = config
        self.qhttpx = QUICKHTTPX(config)

    async def ocstat(self, api_url: str, api_key: str) -> Optional[Dict]:
        url = f"{api_url}/api/integrations/status"
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            async with self.qhttpx._create_http_client(timeout_sec=30) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, ValueError) as exc:
            logger.error(f"owncast fetch status failed: {exc}")
            return None