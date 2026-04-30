import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import httpx
from astrbot.api import AstrBotConfig



async def get_stream_status(owncast_url: str, config: AstrBotConfig) -> Dict[str, Optional[str]]:
