from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api import AstrBotConfig
from .apimain.getapi import OCSTATUS

import httpx

@register("owncast_hook", "ChickenTraicer", "一个 Owncast 播报插件", "0.0.1")
class OwnCastHook(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config


    @filter.command("ocstat")
    async def cmd_ocstat(self, event: AstrMessageEvent):
        url = self.config.get("owncast_url", "").strip()
        params = {"key": self.config.get("owncast_token", "").strip()}
        ocstatus = OCSTATUS(self.config)
        data = await ocstatus.ocstat(url, params["key"])
        logger.info(f"Owncast status: {data}")
        output = ""
        if data != None:
            onlinestat = data.get("online", False)
            title = data.get("streamTitle", "")
            viewer_count = data.get("viewerCount", 0)
        else:
            onlinestat = False
            title = ""
            viewer_count = 0
        output = f"Owncast 在线状态: {'在线' if onlinestat == True else '离线'}"
        if onlinestat == True:
            output += f"\n正在直播: {title}\n观众人数: {viewer_count}"
        yield event.plain_result(output)

        # """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        # user_name = event.get_sender_name()
        # message_str = event.message_str # 用户发的纯文本消息字符串
        # message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        # logger.info(message_chain)
        # yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

    

