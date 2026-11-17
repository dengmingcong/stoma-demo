# stoma-demo

以 Swagger 官方示例 [Petstore](https://petstore3.swagger.io) 为例，说明如何使用 [Stoma](https://github.com/dengmingcong/stoma)。

## 运行示例

### 准备环境

需要 Python 3.12 或更高版本。

克隆本仓库并创建虚拟环境：

```bash
git clone https://github.com/dengmingcong/stoma-demo.git
cd stoma-demo
```

使用 uv 安装依赖：

```bash
uv sync
```

或者使用 pip：

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

> Stoma 使用 Playwright 的 `APIRequestContext` 发送请求，不需要下载浏览器。

### 开始

以下三个步骤演示如何从接口协议得到可调用的接口。

#### 1. 下载接口协议

下载 Petstore 的 OpenAPI 规范文件：

```bash
curl -sL https://petstore3.swagger.io/api/v3/openapi.json -o spec.json
```

本仓库中的 `spec.json` 与该文件内容相同。

#### 2. 生成接口代码

由规范文件生成接口定义：

```bash
uv run stoma spec.json --out app --prefix /api/v3
```

生成结果为 `app/models.py`、`app/router.py` 与 `app/endpoints/` 下的端点代码。
其中 `GetUserByName` 声明了路径参数与响应协议：

```python
@router.get("/user/{username}")
class GetUserByName(APIRoute):
    username: str

    @property
    def on_200_application_json(self) -> ResponseSpec[User]:
        return ResponseSpec(
            status_code=200,
            media_type="application/json",
            expected_type=User,
        )
```

#### 3. 调用接口

导入生成的端点，发送请求并对响应断言：

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

`expect()` 先校验状态码与媒体类型，再将响应体转换为 `User`。响应中的 `firstName`
按模型声明的别名映射到 `first_name`。

演示后端为 Swagger 官方 Petstore 公共服务，由多方共用，可用性不作保证，
可能返回 HTTP 500。

### 运行本仓库的测试

```bash
uv run pytest -v
```

或者使用 pip：

```bash
pytest
```

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

## 反馈

问题与建议：[Stoma Discussions](https://github.com/dengmingcong/stoma/discussions)

许可证：[MIT](https://github.com/dengmingcong/stoma/blob/master/LICENSE)
