"""demo 仓库的 pytest fixtures。

本文件复刻主仓 ``tests/conftest.py`` 中「会话级共享 Playwright 实例」的模式，
理由完全相同：

- ``sync_playwright().start()`` 每次会创建独立的 asyncio loop，跨 fixture
  边界的状态切换会让 Python 缓存的事件循环策略指向已关闭的 loop，后续调用
  ``sync_playwright().start()`` 会看到假活状态而抛出
  ``It looks like you are using Playwright Sync API inside the asyncio loop``。
- 解决方式是让整个 pytest session 共用一个 Playwright 实例 → 共用一个
  asyncio loop，全程没有 loop 切换。

注意：Stoma 只使用 Playwright 的 ``APIRequestContext``，**从不启动浏览器**，
因此这里无需 ``playwright install``，也没有浏览器二进制的下载体积。

演示后端是 Swagger 官方 Petstore 公共服务（``https://petstore3.swagger.io``）。
这是**一个人人共享的公开演示服务，可用性不保证，可能返回 HTTP 500** ——
这是服务状态问题，与 Stoma 无关。测试直接断言真实状态码，
让失败原因一目了然，而不是用重试或跳过把它掩盖掉。
"""

from __future__ import annotations

from collections.abc import Generator

import pytest
from playwright.sync_api import Playwright, sync_playwright

from stoma import Client

__all__ = [
    "_shared_playwright",
    "client",
]

PETSTORE_BASE_URL = "https://petstore3.swagger.io"
"""Petstore 公共服务的根地址。生成的接口自带 ``/api/v3`` 前缀（见 ``app/router.py``）。"""


@pytest.fixture(scope="session")
def _shared_playwright() -> Generator[Playwright, None, None]:
    """会话级共享的 Playwright 实例。

    整个 pytest session 内共用同一个 Playwright runtime 与 asyncio loop，
    避免 ``sync_playwright().start()`` 多次启动造成的事件循环状态污染。
    session 结束时统一 ``stop()`` 释放资源。
    """
    playwright_instance: Playwright = sync_playwright().start()
    try:
        yield playwright_instance
    finally:
        playwright_instance.stop()


@pytest.fixture(scope="session")
def client(_shared_playwright: Playwright) -> Client:
    """绑定到 Petstore 的 Stoma 客户端。

    使用 ``APIRequestContext``（而非浏览器上下文），因此不涉及浏览器启动。
    """
    context = _shared_playwright.request.new_context(base_url=PETSTORE_BASE_URL)
    return Client(context=context)
