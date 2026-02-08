"""
Base schemas with UUID serialization support
"""
from pydantic import BaseModel, ConfigDict
from typing import Any
import uuid


class BaseResponseModel(BaseModel):
    """Base model for all response schemas with UUID serialization"""

    model_config = ConfigDict(
        from_attributes=True,
        # Use a custom JSON encoder for UUID types
        json_encoders={uuid.UUID: str}
    )
