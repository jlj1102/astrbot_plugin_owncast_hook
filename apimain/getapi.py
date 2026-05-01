from astrbot.api import AstrBotConfig
from astrbot.api import logger

import asyncio
from typing import Dict, List, Optional, Tuple
import httpx

from .qchttpx import QUICKHTTPX

class OCSTATUS:
    def __init__(self, config: AstrBotConfig):
        self.config = config
        self.qhttpx = QUICKHTTPX(config)
        self.last_disconnect_time = None  # Persistent storage for lastDisconnectTime

    async def ocstat(self, api_url: str, api_key: str) -> Optional[Dict]:
        url = f"{api_url}/api/integrations/status"
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            async with self.qhttpx._create_http_client(timeout_sec=self.config.get("timeout", 10)) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data
        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, ValueError) as exc:
            logger.error(f"owncast fetch status failed: {exc}")
            return None
        
    async def dataparse(self, data: Optional[Dict]) -> Dict:
        """Parse Owncast API response and return standardized variables"""
        if data is None:
            return {
                "isonline": False,
                "title": "",
                "viewer_count": 0,
                "lastconnect": "",
                "lastdisconnect": self.last_disconnect_time,
                "version_number": "",
                "overall_max_viewer_count": 0,
                "session_max_viewer_count": 0
            }

        # Update persistent lastDisconnectTime if present in data
        if data.get("lastDisconnectTime") is not None:
            self.last_disconnect_time = data.get("lastDisconnectTime")

        return {
            "isonline": data.get("online", False),
            "title": data.get("streamTitle", ""),
            "viewer_count": data.get("viewerCount", 0),
            "lastconnect": data.get("lastConnectTime", ""),
            "lastdisconnect": self.last_disconnect_time,
            "version_number": data.get("versionNumber", ""),
            "overall_max_viewer_count": data.get("overallMaxViewerCount", 0),
            "session_max_viewer_count": data.get("sessionMaxViewerCount", 0)
        }