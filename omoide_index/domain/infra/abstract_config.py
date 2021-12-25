# -*- coding: utf-8 -*-
"""Infrastructure."""
import abc


class AbstractConfig(abc.ABC):
    """Base class for settings checking."""

    @abc.abstractmethod
    def is_on(self, variable: str) -> bool:
        """Return True if variable with this name is active."""

    @abc.abstractmethod
    def get_value(self, variable: str) -> str:
        """Return value of the variable."""
