from typing import Any
from pydantic import BaseModel, Field


class APIResponseMetadata(BaseModel):
    placeholder: str = "Insert pagination, sorting, filtering, etc. here"


class APIResponse(BaseModel):
    data: Any
    metadata: APIResponseMetadata = Field(APIResponseMetadata(), alias="_metadata")
