# -*- coding: utf-8 -*-
"""Search related use cases.
"""
from omoide_index import domain

__all__ = [
    'SearchRandomItemsUseCase',
    'SearchSpecificItemsUseCase',
]


class SearchRandomItemsUseCase:
    """No query specified, user wants random images."""

    def __init__(
            self,
            query: domain.Query,
            index: domain.Index,
    ) -> None:
        """Initialize instance."""
        self.query = query
        self.index = index

    def execute(self) -> domain.SearchResult:
        """Execute use case."""
        # TODO
        return domain.SearchResult(
            items=[],
            page=1,
            total_pages=1,
            announce='',
        )


class SearchSpecificItemsUseCase:
    """Search by given tags."""

    def __init__(
            self,
            query: domain.Query,
            index: domain.Index,
    ) -> None:
        """Initialize instance."""
        self.query = query
        self.index = index

    def execute(self) -> domain.SearchResult:
        """Execute use case."""
        # TODO
        return domain.SearchResult(
            items=[],
            page=1,
            total_pages=1,
            announce='',
        )
