"""Generated event models from CDP specification"""
# Domain: WebAudio Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class ContextcreatedEvent(CDPModel):
    """Notifies that a new BaseAudioContext has been created."""

    context: BaseAudioContext


class ContextwillbedestroyedEvent(CDPModel):
    """Notifies that an existing BaseAudioContext will be destroyed."""

    context_id: GraphObjectId


class ContextchangedEvent(CDPModel):
    """Notifies that existing BaseAudioContext has changed some properties (id stays the same).."""

    context: BaseAudioContext


class AudiolistenercreatedEvent(CDPModel):
    """Notifies that the construction of an AudioListener has finished."""

    listener: AudioListener


class AudiolistenerwillbedestroyedEvent(CDPModel):
    """Notifies that a new AudioListener has been created."""

    context_id: GraphObjectId
    listener_id: GraphObjectId


class AudionodecreatedEvent(CDPModel):
    """Notifies that a new AudioNode has been created."""

    node: AudioNode


class AudionodewillbedestroyedEvent(CDPModel):
    """Notifies that an existing AudioNode has been destroyed."""

    context_id: GraphObjectId
    node_id: GraphObjectId


class AudioparamcreatedEvent(CDPModel):
    """Notifies that a new AudioParam has been created."""

    param: AudioParam


class AudioparamwillbedestroyedEvent(CDPModel):
    """Notifies that an existing AudioParam has been destroyed."""

    context_id: GraphObjectId
    node_id: GraphObjectId
    param_id: GraphObjectId


class NodesconnectedEvent(CDPModel):
    """Notifies that two AudioNodes are connected."""

    context_id: GraphObjectId
    source_id: GraphObjectId
    destination_id: GraphObjectId
    source_output_index: float | None = None
    destination_input_index: float | None = None


class NodesdisconnectedEvent(CDPModel):
    """Notifies that AudioNodes are disconnected. The destination can be null, and it means all the outgoing connections from the source are disconnected."""

    context_id: GraphObjectId
    source_id: GraphObjectId
    destination_id: GraphObjectId
    source_output_index: float | None = None
    destination_input_index: float | None = None


class NodeparamconnectedEvent(CDPModel):
    """Notifies that an AudioNode is connected to an AudioParam."""

    context_id: GraphObjectId
    source_id: GraphObjectId
    destination_id: GraphObjectId
    source_output_index: float | None = None


class NodeparamdisconnectedEvent(CDPModel):
    """Notifies that an AudioNode is disconnected to an AudioParam."""

    context_id: GraphObjectId
    source_id: GraphObjectId
    destination_id: GraphObjectId
    source_output_index: float | None = None
