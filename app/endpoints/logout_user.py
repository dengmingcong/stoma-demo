"""Logs out current logged in user session.。

Generated from OpenAPI: logoutUser
Log user out of the system.
"""
from __future__ import annotations

from typing import Annotated
from pydantic import Field
from stoma import APIRoute, ResponseSpec, EmptyResponseSpec, Header, Body, Form, UploadFile

from ..router import router

@router.get("/user/logout")
class LogoutUser(APIRoute):
    """Logs out current logged in user session.。

Log user out of the system.
"""
    @property
    def on_200(self) -> EmptyResponseSpec:
        return EmptyResponseSpec(
            status_code=200,
        )
    @property
    def on_default(self) -> EmptyResponseSpec:
        return EmptyResponseSpec(
            status_code=lambda c: c not in [200],
        )
