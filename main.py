from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig
from apimain import getapi

import httpx

@register("owncast_hook", "ChickenTraicer", "一个利用 Owncast Webhook 进行网页播报的插件", "0.0.1")
class OwnCastHook(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config


    @filter.command("ocstat")
    async def cmd_ocstat(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

    
    def _get_proxy_url(self) -> str:
        return str(self.config.get("proxy_url", "")).strip()

    def _create_http_client(self, timeout_sec: int, follow_redirects: bool = False) -> httpx.AsyncClient:
        proxy_url = self._get_proxy_url()
        verify_ssl = False
        kwargs = {
            "timeout": timeout_sec,
            "follow_redirects": follow_redirects,
            "verify": verify_ssl,
        }
        if proxy_url:
            try:
                return httpx.AsyncClient(proxy=proxy_url, **kwargs)
            except TypeError:
                return httpx.AsyncClient(proxies=proxy_url, **kwargs)
        return httpx.AsyncClient(**kwargs)

