"""Generated from CDP specification"""
# Domain: ServiceWorker

from typing import Any, Literal
from pydantic_cpd.cdp.base import CDPModel

RegistrationID = str


class ServiceWorkerRegistration(CDPModel):
    """ServiceWorker registration."""

    registration_id: RegistrationID
    scope_u_r_l: str
    is_deleted: bool


ServiceWorkerVersionRunningStatus = Literal[
    "stopped", "starting", "running", "stopping"
]

ServiceWorkerVersionStatus = Literal[
    "new", "installing", "installed", "activating", "activated", "redundant"
]


class ServiceWorkerVersion(CDPModel):
    """ServiceWorker version."""

    version_id: str
    registration_id: RegistrationID
    script_u_r_l: str
    running_status: ServiceWorkerVersionRunningStatus
    status: ServiceWorkerVersionStatus
    script_last_modified: float | None = None
    script_response_time: float | None = None
    controlled_clients: list[Target.TargetID] | None = None
    target_id: target.TargetID | None = None
    router_rules: str | None = None


class ServiceWorkerErrorMessage(CDPModel):
    """ServiceWorker error message."""

    error_message: str
    registration_id: RegistrationID
    version_id: str
    source_u_r_l: str
    line_number: int
    column_number: int
