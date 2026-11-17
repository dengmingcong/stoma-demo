# stoma-demo

以 [Petstore](https://petstore3.swagger.io) 为例，说明如何使用 [Stoma](https://github.com/dengmingcong/stoma)。

- `spec.json` - Petstore 的 OpenAPI 规范，下载自 [petstore3.swagger.io/api/v3/openapi.json](https://petstore3.swagger.io/api/v3/openapi.json)。
- `app/` - Stoma CLI 根据 `spec.json` 生成的接口定义。
- `tests/` - 展示在 Stoma 中如何调用接口。

## 运行

需要 Python 3.12 或更高版本：

```bash
git clone https://github.com/dengmingcong/stoma-demo.git
cd stoma-demo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

> 💡 如果安装了 `uv`，则使用 `uv` 更简单。
> ⚠️ Swagger 官方 Petstore 不稳定，可能返回 HTTP 500 导致用例失败。

## 真实项目

在自己项目中使用 Stoma。

1. 下载接口协议

    ```bash
    curl -sL https://petstore3.swagger.io/api/v3/openapi.json -o spec.json
    ```
2. 生成接口代码

    ```bash
    stoma spec.json --out app --prefix /api/v3
    ```

3. 调用接口

    导入生成的接口，发送请求并对响应断言：

    ```python
    from playwright.sync_api import sync_playwright
    from stoma import Client
    from app.endpoints.get_user_by_name import GetUserByName

    with sync_playwright() as p:
        ctx = p.request.new_context(base_url="https://petstore3.swagger.io")
        client = Client(context=ctx)

        endpoint = GetUserByName(username="user1")
        response = client.send(endpoint)
        user = response.expect(endpoint.on_200_application_json)
        assert user.username == "user1"
    ```

## 反馈

问题与建议：[Stoma Discussions](https://github.com/dengmingcong/stoma/discussions)

许可证：[MIT](https://github.com/dengmingcong/stoma/blob/master/LICENSE)
