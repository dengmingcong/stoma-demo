# stoma-demo

[Stoma](https://github.com/dengmingcong/stoma) 的可运行示例 —— 用「代码即协议」的方式
定义接口、调用接口、对响应断言。

## 运行示例

`spec.json` 为 [Swagger 官方 Petstore](https://petstore3.swagger.io/api/v3/openapi.json)
的规范文件。`app/` 是依据该规范生成的接口定义，`tests/` 是针对这些接口定义编写的测试。

需要 Python 3.12 或更高版本。

```bash
git clone https://github.com/dengmingcong/stoma-demo.git
cd stoma-demo
uv sync
uv run pytest -v
```

或者使用 pip：

```bash
git clone https://github.com/dengmingcong/stoma-demo.git
cd stoma-demo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

> Stoma 使用 Playwright 的 `APIRequestContext` 发送请求，不需要下载浏览器。

演示后端为 Swagger 官方 Petstore 公共服务，由多方共用，可用性不作保证，
可能返回 HTTP 500。

## 说明

| 端点 | 说明 |
|------|------|
| `GET /user/{username}` | 路径参数、多状态码响应协议、字段别名映射 |
| `GET /pet/findByStatus` | 查询参数、列表响应、错误分支 |
| `GET /user/login` | 多个查询参数 |
| `GET /user/logout` | 无参数端点 |
| `POST /pet` | 请求体 |
| `POST /pet/{petId}` | 路径参数与查询参数组合 |
| `POST /store/order` | 请求体与类型化响应 |

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

`expect()` 先校验状态码与媒体类型，再将响应体转换为 `User`。响应中的 `firstName`
按模型声明的别名映射到 `first_name`。

## 反馈

问题与建议：[Stoma Discussions](https://github.com/dengmingcong/stoma/discussions)

许可证：[MIT](https://github.com/dengmingcong/stoma/blob/master/LICENSE)
