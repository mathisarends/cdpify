"""CDP DOMDebugger Domain"""

from .types import *
from .commands import *
from .events import *
from .client import DOMDebuggerClient

__all__ = ["DOMDebuggerClient"]
