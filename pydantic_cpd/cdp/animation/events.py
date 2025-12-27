"""Generated event models from CDP specification"""
# Domain: Animation Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class AnimationcanceledEvent(CDPModel):
    """Event for when an animation has been cancelled."""

    id: str


class AnimationcreatedEvent(CDPModel):
    """Event for each animation that has been created."""

    id: str


class AnimationstartedEvent(CDPModel):
    """Event for animation that has been started."""

    animation: Animation


class AnimationupdatedEvent(CDPModel):
    """Event for animation that has been updated."""

    animation: Animation
