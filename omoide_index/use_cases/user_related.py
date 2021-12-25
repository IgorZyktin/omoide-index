# -*- coding: utf-8 -*-
"""User and permission related use cases.
"""
from omoide_index import domain

__all__ = [
    'RefreshUserUseCase',
    'DropUserUseCase',
]


class RefreshUserUseCase:
    """Create/update user."""

    def __init__(
            self,
            model: domain.UserRefreshModel,
            index: domain.Index,
            status: domain.Status,
    ) -> None:
        """Initialize instance."""
        self.model = model
        self.index = index
        self.status = status

    def execute(self) -> None:
        """Execute use case."""
        # TODO
        return


class DropUserUseCase:
    """Delete user."""

    def __init__(
            self,
            model: domain.UserDropModel,
            index: domain.Index,
            status: domain.Status,
    ) -> None:
        """Initialize instance."""
        self.model = model
        self.index = index
        self.status = status

    def execute(self) -> None:
        """Execute use case."""
        # TODO
        return
