from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register, StarTools
from astrbot.api import logger
from astrbot.api import AstrBotConfig
from astrbot.api.message_components import Plain
from astrbot.core.message.message_event_result import MessageChain

import asyncio
import contextlib

from .apimain.getapi import OCSTATUS

@register("owncast_hook", "ChickenTraicer", "一个 Owncast 播报插件", "0.0.1")
class OwnCastHook(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self._stop_event = asyncio.Event()
        self._task = asyncio.create_task(self.autoreq())
        self.online_status = None  # Store last known online status to detect changes
        self.advancedcfg = config.get("advanced", {})
        


    @filter.command("owncast_stat")
    async def cmd_ocstat(self, event: AstrMessageEvent):
        url = self.config.get("owncast_url", "").strip()
        api_key = self.config.get("owncast_token", "").strip()
        ocstatus = OCSTATUS(self.config)

        data = await ocstatus.ocstat(url, api_key)
        parsed = await ocstatus.dataparse(data)

        logger.info(f"Owncast status: {parsed}")

        output = f"Owncast 在线状态: {'在线' if parsed['isonline'] else '离线'}"
        if parsed['isonline']:
            output += f"\n正在直播: {parsed['title']}\n观众人数: {parsed['viewer_count']}\n直播开始时间: {parsed['lastconnect']}"
        else:
            output += f"\n上次直播结束时间: {parsed['lastdisconnect']}"

        yield event.plain_result(output)

    async def autoreq(self):
        if not self.config.get("owncast_url", "").strip() or not self.config.get("owncast_token", "").strip():
            logger.warning("Owncast URL or API token not configured, skipping autoreq.")
            return
        if self.config.get("owncast_autorequest", False) is not True:
            logger.info("Owncast autorequest is disabled in config, skipping autoreq.")
            return
        while not self._stop_event.is_set():
            try:
                await self.onereq()
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("steamwatch poll loop error")
            interval = max(5, int(self.config.get("request_delay", 60)))
            try:
                await asyncio.wait_for(self._stop_event.wait(), timeout=interval)
            except asyncio.TimeoutError:
                continue


    async def onereq(self):
        url = self.config.get("owncast_url", "").strip()
        api_key = self.config.get("owncast_token", "").strip()
        ocstatus = OCSTATUS(self.config)
        data = await ocstatus.ocstat(url, api_key)
        parsed = await ocstatus.dataparse(data)
        logger.debug(f"Owncast status: {parsed}")
        if self.online_status is None:
            self.online_status = parsed['isonline']
        elif parsed['isonline'] != self.online_status:
            self.online_status = parsed['isonline']
            if parsed['isonline'] is True:
                watch_url = self.advancedcfg.get('external_owncast_url', '').strip() or self.config.get("owncast_url", "").strip()
                message = f"{self.config.get('owncast_user', 'user')}的 Owncast 直播开始了！\n正在直播: {parsed['title']}\n观看地址: {watch_url}"
                await self.senderreq(message)

    async def senderreq(self, message: str):
        """Send message to configured QQ groups using StarTools"""
        for group in self.config.get("request_qq_group", []):
            try:
                message_chain = MessageChain(chain=[Plain(message)])
                await StarTools.send_message_by_id(
                    type="GroupMessage",
                    id=str(group),
                    message_chain=message_chain,
                    platform="aiocqhttp"
                )
                logger.info(f"Sent Owncast notification to group {group}")
            except Exception as e:
                logger.error(f"Failed to send message to group {group}: {e}")
        
    async def terminate(self):
        self._stop_event.set()
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
    

