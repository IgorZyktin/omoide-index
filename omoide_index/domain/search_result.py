# -*- coding: utf-8 -*-
"""Search result.
"""

from pydantic import BaseModel

__all__ = [
    'SearchResult',
]


class SearchResult(BaseModel):
    """Search result."""
    items: list[str]
    page: int
    total_pages: int
    total_items: int
    announce: str
