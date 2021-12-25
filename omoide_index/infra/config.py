# -*- coding: utf-8 -*-
"""Infrastructure."""
import os

from omoide_index.domain import infra as domain_infra


class Config(domain_infra.AbstractConfig):
    """Settings management."""

    def is_on(self, variable: str) -> bool:
        """Return True if variable with this name is active."""
        return os.environ.get(variable) in ('yes', 'True', 'true', '1')

    def get_value(self, variable: str) -> str:
        """Return value of the variable."""
        value = os.environ.get(variable)

        if value is None:
            raise ValueError(f'No variable named {variable!r} found')

        return value
