"""Generated event models from CDP specification"""
# Domain: Media Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class PlayerpropertieschangedEvent(CDPModel):
    """This can be called multiple times, and can be used to set / override /
    remove player properties. A null propValue indicates removal."""

    player_id: PlayerId
    properties: list[PlayerProperty]


class PlayereventsaddedEvent(CDPModel):
    """Send events as a list, allowing them to be batched on the browser for less
    congestion. If batched, events must ALWAYS be in chronological order."""

    player_id: PlayerId
    events: list[PlayerEvent]


class PlayermessagesloggedEvent(CDPModel):
    """Send a list of any messages that need to be delivered."""

    player_id: PlayerId
    messages: list[PlayerMessage]


class PlayererrorsraisedEvent(CDPModel):
    """Send a list of any errors that need to be delivered."""

    player_id: PlayerId
    errors: list[PlayerError]


class PlayercreatedEvent(CDPModel):
    """Called whenever a player is created, or when a new agent joins and receives
    a list of active players. If an agent is restored, it will receive one
    event for each active player."""

    player: Player
