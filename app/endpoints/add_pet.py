"""Add a new pet to the store.。

Generated from OpenAPI: addPet
Add a new pet to the store.
"""
from __future__ import annotations

from typing import Annotated
from pydantic import Field
from stoma import APIRoute, ResponseSpec, EmptyResponseSpec, Header, Body, Form, UploadFile

from ..router import router

from ..models import Pet
@router.post("/pet")
class AddPet(APIRoute):
    """Add a new pet to the store.。

Add a new pet to the store.
"""
    body: Pet
    @property
    def on_200_application_json(self) -> ResponseSpec[Pet]:
        return ResponseSpec(
            status_code=200,
            media_type="application/json",
            expected_type=Pet,
        )
    @property
    def on_200_application_xml(self) -> ResponseSpec[Pet]:
        return ResponseSpec(
            status_code=200,
            media_type="application/xml",
            expected_type=Pet,
        )
    @property
    def on_400(self) -> EmptyResponseSpec:
        return EmptyResponseSpec(
            status_code=400,
        )
    @property
    def on_422(self) -> EmptyResponseSpec:
        return EmptyResponseSpec(
            status_code=422,
        )
    @property
    def on_default(self) -> EmptyResponseSpec:
        return EmptyResponseSpec(
            status_code=lambda c: c not in [200, 400, 422],
        )
