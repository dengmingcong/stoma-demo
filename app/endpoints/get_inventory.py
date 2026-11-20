"""Returns pet inventories by status.。

Generated from OpenAPI: getInventory
Returns a map of status codes to quantities.
"""
from __future__ import annotations

from typing import Annotated
from pydantic import Field
from stoma import APIRoute, ResponseSpec, EmptyResponseSpec, Header, Body, Form, UploadFile

from ..router import router

from ..models import GetInventoryResponse
@router.get("/store/inventory")
class GetInventory(APIRoute):
    """Returns pet inventories by status.。

Returns a map of status codes to quantities.
"""
    @property
    def on_200(self) -> ResponseSpec[GetInventoryResponse]:
        return ResponseSpec(
            status_code=200,
            media_type="application/json",
            expected_type=GetInventoryResponse,
        )
    @property
    def on_default(self) -> EmptyResponseSpec:
        return EmptyResponseSpec(
            status_code=lambda c: c not in [200],
        )
