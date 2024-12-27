"""
Utility functions related to handling exceptions
"""
import sys


def except_hook(cls, exception, traceback):
    """
    Exception hook to enable stderr exceptions output for PyQt application

    Args:
        cls (Type[BaseException]): exception class
        exception (BaseException): exception value
        traceback (Optional[TracebackType]): traceback

    Returns:
        None
    """
    sys.__excepthook__(cls, exception, traceback)
