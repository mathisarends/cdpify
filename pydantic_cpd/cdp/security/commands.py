"""Generated command models from CDP specification"""

from pydantic_cpd.cdp.base import CDPModel

from .types import *

class SetIgnoreCertificateErrorsParams(CDPModel):
    """
    Enable/disable whether all certificate errors should be ignored.
    """
    ignore: bool

class HandleCertificateErrorParams(CDPModel):
    """
    Handles a certificate error that fired a certificateError event.
    """
    event_id: int
    action: CertificateErrorAction

class SetOverrideCertificateErrorsParams(CDPModel):
    """
    Enable/disable overriding certificate errors. If enabled, all certificate error
    events need to be handled by the DevTools client and should be answered with
    `handleCertificateError` commands.
    """
    override: bool
