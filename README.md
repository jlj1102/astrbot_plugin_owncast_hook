# astrbot-plugin-owncast-hook

一个简单Astrbot自动发送和获取Owncast直播信息的插件

> [!NOTE]
> 这个repo可能需要较高版本的Astrbot
>
> 暂时这个插件只适配于aiocqhttp控制器

## 前置
该插件所需的apikey需要在Owncast网站管理的 /admin/access-tokens/ 界面添加一个token，需要给予管理权限以获取服务器状态

这个插件依赖于Python的httpx (别问为啥，问就是httpx字段的代码一部分是借鉴来的)

## 配置文件设置
- `owncast_user`: Owncast用户名，在发送消息时显示
- `owncast_url`: Owncast主链接，api访问时使用这个链接
- `owncast_token`: Owncast管理token
- `owncast_autorequest`: 是否自动获取状态
- `request_qq_group`: 发送自动获取的QQ群
- `request_delay`: 请求间隔时间
- `timeout`: 请求超时时间
- `external_owncast_url`: 外部Owncast链接，发送消息时会发送的链接，留空则为主链接
- `proxy_url`: 代理链接
- `verify_ssl`: 是否验证SSL证书

# Supports

- [AstrBot Repo](https://github.com/AstrBotDevs/AstrBot)
- [Owncast Repo](https://github.com/owncast/owncast)
- [Owncast Documentation](https://owncast.online/docs/)
