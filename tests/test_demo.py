"""demo 示例的断言测试。

覆盖「定义接口 → 调用 → 断言」的完整链路：接口定义由 ``app/`` 下的
OpenAPI 生成代码提供，本文件只负责调用与断言。

演示后端是 Swagger 官方 Petstore 公共服务（``https://petstore3.swagger.io``），
``spec.json`` 是它的**原始规范**，未做任何删改。
选用的端点覆盖 Stoma 的主要特性：

============================  ==========================================
端点                          展示的特性
============================  ==========================================
``GET /user/{username}``      path 参数、多状态码响应协议、类型化响应
``GET /pet/findByStatus``     query 参数、列表响应、错误分支
``GET /user/login``           多个 query 参数
``GET /user/logout``          无参数端点
``POST /pet``                 body 请求体
``POST /pet/{petId}``         path 参数 + query 参数组合
============================  ==========================================

**关于服务稳定性**：Petstore 是**公共演示服务**，可用性不保证，
**可能出现 HTTP 500**。这是服务状态问题，与 Stoma 无关 ——
测试直接断言真实状态码，让失败原因一目了然，不用重试或跳过把它掩盖掉。
"""

from __future__ import annotations

from stoma import Client

from app.endpoints.add_pet import AddPet
from app.endpoints.find_pets_by_status import FindPetsByStatus
from app.endpoints.get_user_by_name import GetUserByName
from app.endpoints.login_user import LoginUser
from app.endpoints.logout_user import LogoutUser
from app.endpoints.place_order import PlaceOrder
from app.endpoints.update_pet_with_form import UpdatePetWithForm
from app.models import Order, Pet, User


def test_get_user_by_name(client: Client) -> None:
    """按用户名查询 —— path 参数 + 多状态码响应协议。

    ``on_200`` 声明了带类型的成功响应，``expect()`` 会把响应体转成 ``User``；
    ``on_404`` 是空响应协议，只校验状态码。

    注意 ``User.first_name`` 声明了别名 ``firstName`` —— 响应体里的
    ``firstName`` 会被自动映射到 Python 侧的 ``first_name``。
    """
    endpoint = GetUserByName(username="user1")

    response = client.send(endpoint)

    user = response.expect(endpoint.on_200_application_json)
    assert isinstance(user, User)
    assert user.username == "user1"
    assert user.id is not None
    assert user.first_name == "first name 1"


def test_find_pets_by_status(client: Client) -> None:
    """按状态查询宠物 —— query 参数 + 列表响应。

    响应是 ``list[Pet]``，生成的模型是一个 ``RootModel``。
    该端点在规范里声明了多个 media type，因此生成了
    ``on_200_application_json`` 与 ``on_200_application_xml`` 两套响应协议。
    """
    endpoint = FindPetsByStatus(status="available")

    response = client.send(endpoint)

    pets = response.expect(endpoint.on_200_application_json)
    assert isinstance(pets.root, list)
    assert all(isinstance(pet, Pet) for pet in pets.root)


def test_find_pets_by_status_bad_request(client: Client) -> None:
    """非法 status —— 走 ``on_400`` 分支。

    这是「同一份接口定义覆盖多种响应」的直接演示：
    200 与 400 用同一套声明，只是断言时取不同的协议。
    """
    endpoint = FindPetsByStatus(status="not-a-valid-status")

    response = client.send(endpoint)

    response.expect(endpoint.on_400)


def test_login(client: Client) -> None:
    """登录 —— 多个 query 参数，标量响应。"""
    endpoint = LoginUser(username="stoma-demo", password="stoma-demo")

    response = client.send(endpoint)

    session = response.expect(endpoint.on_200_application_json)
    assert isinstance(session, str)


def test_logout(client: Client) -> None:
    """登出 —— 无参数端点。"""
    endpoint = LogoutUser()

    response = client.send(endpoint)

    response.expect(endpoint.on_200)


def test_add_pet(client: Client) -> None:
    """创建宠物 —— body 请求体。

    ``body`` 参数的类型是生成的 ``Pet`` 模型，
    请求体由 Pydantic 序列化（含 ``photoUrls`` 等字段别名）。
    """
    endpoint = AddPet(body=Pet(name="stoma-demo-pet", photoUrls=[]))

    response = client.send(endpoint)

    created = response.expect(endpoint.on_200_application_json)
    assert isinstance(created, Pet)
    assert created.name == "stoma-demo-pet"


def test_place_order(client: Client) -> None:
    """下单 —— body 请求体 + 标量响应。

    ``Order`` 模型声明了 ``shipDate`` 等带别名的字段，
    请求体由 Pydantic 按别名序列化。
    """
    endpoint = PlaceOrder(
        body=Order(id=1, petId=1, quantity=1, status="placed", complete=True)
    )

    response = client.send(endpoint)

    order = response.expect(endpoint.on_200)
    assert isinstance(order, Order)
    assert order.status == "placed"


def test_update_pet_with_form(client: Client) -> None:
    """更新宠物 —— path 参数 + query 参数组合。

    ``pet_id`` 走路径，``name`` 与 ``status`` 走查询参数。
    """
    endpoint = UpdatePetWithForm(
        pet_id=1,
        name="stoma-demo-pet",
        status="available",
    )

    response = client.send(endpoint)

    response.expect(endpoint.on_200_application_json)
