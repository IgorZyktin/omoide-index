# -*- coding: utf-8 -*-
"""Index and database related use cases.
"""
from omoide_index import domain
from omoide_index.domain import infra as domain_infra

__all__ = [
    'CreateIndexOnStartUseCase',
    'ReloadIndexUseCase',
    'RefreshIndexUseCase',
]


class CreateIndexOnStartUseCase:
    """When server is started and no index exists at the moment."""

    # noinspection PyMethodMayBeStatic
    def execute(self) -> domain.Index:
        """Execute use case."""
        return domain.Index()


class ReloadIndexUseCase:
    """Full index reload."""

    def __init__(
            self,
            index: domain.Index,
            status: domain.Status,
            clock: domain_infra.AbstractClock,
            memory_calculator: domain_infra.AbstractMemoryCalculator,
            version: str,
    ) -> None:
        """Initialize instance."""
        self.index = index
        self.status = status
        self.clock = clock
        self.memory_calculator = memory_calculator
        self.version = version

    def execute(self) -> None:
        """Execute use case."""
        # TODO
        return


class RefreshIndexUseCase:
    """Partial index refresh."""

    def __init__(
            self,
            model: domain.IndexRefreshModel,
            index: domain.Index,
            status: domain.Status,
            clock: domain_infra.AbstractClock,
            memory_calculator: domain_infra.AbstractMemoryCalculator,
            version: str,
    ) -> None:
        """Initialize instance."""
        self.model = model
        self.index = index
        self.status = status
        self.clock = clock
        self.memory_calculator = memory_calculator
        self.version = version

    def execute(self) -> None:
        """Execute use case."""
        # TODO
        return
