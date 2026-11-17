# stoma-demo

[Stoma](https://github.com/dengmingcong/stoma) 的可运行示例 —— 用「代码即协议」的方式
定义接口、调用接口、对响应断言。

这个仓库展示一件事：**接口协议写一次，调用和断言就都用它。**

```python
endpoint = GetUserByName(username="user1")
response = client.send(endpoint)
user = response.expect(endpoint.on_200_application_json)
assert user.username == "user1"
```

`GetUserByName` 由 OpenAPI 规范生成，它同时声明了请求参数（`username`）和响应协议
（`on_200_application_json`）—— 上面三行用的就是这份声明。

## 运行

需要 Python 3.12 或更高版本。

```bash
git clone https://github.com/dengmingcong/stoma-demo.git
cd stoma-demo
uv sync
uv run pytest -v
```

没有 uv 也可以走 pip：

```bash
git clone https://github.com/dengmingcong/stoma-demo.git
cd stoma-demo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

> **不需要安装浏览器。** Stoma 只用 Playwright 的 `APIRequestContext` 发请求，
> 从不启动浏览器 —— 所以没有 `playwright install` 这一步，也没有浏览器组件的下载体积。
> 这对 API 测试是个实打实的优势：CI 镜像不用为浏览器付出几百 MB。

## 示例内容

`spec.json` 是 [Swagger 官方 Petstore](https://petstore3.swagger.io/api/v3/openapi.json)
的原始规范（未做任何删改）。`app/` 是从它生成的接口定义，`tests/` 是对生成代码的断言。

| 端点 | 展示的特性 |
|------|-----------|
| `GET /user/{username}` | path 参数、多状态码响应协议、带别名的类型化响应 |
| `GET /pet/findByStatus` | query 参数、列表响应、错误分支 |
| `GET /user/login` | 多个 query 参数 |
| `GET /user/logout` | 无参数端点 |
| `POST /pet` | body 请求体 |
| `POST /pet/{petId}` | path 参数 + query 参数组合 |
| `POST /store/order` | body 请求体 + 类型化响应 |

断言就是最普通的 pytest 断言：

```python
def test_get_user_by_name(client: Client) -> None:
    endpoint = GetUserByName(username="user1")

    response = client.send(endpoint)

    user = response.expect(endpoint.on_200_application_json)
    assert isinstance(user, User)
    assert user.username == "user1"
    assert user.id is not None
    assert user.first_name == "first name 1"
```

`expect()` 会先校验 Status Code 与 Media type，再把响应体转成 `User`。
响应里的 `firstName` 按模型声明的别名映射到 `first_name`。

## 重新生成接口代码

`app/` 里的代码是从 `spec.json` 生成的。规范更新后重新生成：

```bash
uv run stoma spec.json --out app --prefix /api/v3
```

生成结果的 `models.py` 头部带一个 codegen 时间戳，因此每次生成都会有细微差异 ——
比对时先归一化掉那一行：

```bash
uv run stoma spec.json --out app --prefix /api/v3
sed '/^#   timestamp:/d' app/models.py > /tmp/new.py
sed '/^#   timestamp:/d' <已提交的 app/models.py> > /tmp/old.py
diff /tmp/old.py /tmp/new.py
```

## 关于演示后端

演示后端是 **Swagger 官方 Petstore 公共服务**（`https://petstore3.swagger.io`），
不是本地 mock。

它是**人人共享的公开演示服务，可用性不保证，可能返回 HTTP 500** —— 实测中出现过
`POST /pet`、`GET /pet/{petId}`、`GET /store/inventory` 等端点持续 500 的情况，
等待数分钟也不恢复。这是服务状态问题，与 Stoma 无关。

测试直接断言真实状态码，不做重试或跳过 —— 所以你看到的失败信息会明确指出
「期望 200，实际为 500」，而不是被掩盖成别的样子。

## 反馈

问题与建议：[Stoma Discussions](https://github.com/dengmingcong/stoma/discussions)

许可证：[MIT](https://github.com/dengmingcong/stoma/blob/master/LICENSE)
