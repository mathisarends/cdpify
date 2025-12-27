"""Generated event models from CDP specification"""
# Domain: ServiceWorker Events

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

from .types import *


class WorkererrorreportedEvent(CDPModel):
    error_message: ServiceWorkerErrorMessage


class WorkerregistrationupdatedEvent(CDPModel):
    registrations: list[ServiceWorkerRegistration]


class WorkerversionupdatedEvent(CDPModel):
    versions: list[ServiceWorkerVersion]
