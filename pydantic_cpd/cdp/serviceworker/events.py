"""Generated event models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class WorkerErrorReportedEvent(CDPModel):
    error_message: ServiceWorkerErrorMessage

class WorkerRegistrationUpdatedEvent(CDPModel):
    registrations: list[ServiceWorkerRegistration]

class WorkerVersionUpdatedEvent(CDPModel):
    versions: list[ServiceWorkerVersion]
