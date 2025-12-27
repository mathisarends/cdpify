"""Generated CDP base models"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CDPModel(BaseModel):
    """Base model for CDP with automatic camelCase alias generation."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )
