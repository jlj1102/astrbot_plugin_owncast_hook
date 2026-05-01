import httpx
from astrbot.api import AstrBotConfig

class QUICKHTTPX:
    def __init__(self, config: AstrBotConfig):
        self.config = config

    def _get_proxy_url(self) -> str:
        return str(self.config.get("proxy_url", "")).strip()

    def _create_http_client(self, timeout_sec: int, follow_redirects: bool = False) -> httpx.AsyncClient:
        proxy_url = self._get_proxy_url()
        verify_ssl = self.config.get("verify_ssl", True)
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
