# -*- coding: utf-8 -*-
"""`credit_manager.errors` module.

Provides Error Hierarchy classes.
"""


class BaseError(Exception):
    """Base project Error class.
    """
    pass


class ModelError(BaseError):
    """Raises when a `credit_manager.models` error occurs.
    """
    pass


class UtilsError(BaseError):
    """Raises when a `credit_manager.utils` error occurs.
    """
    pass
