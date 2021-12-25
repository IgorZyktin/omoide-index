# -*- coding: utf-8 -*-
"""Search query.
"""

from pydantic import BaseModel

__all__ = [
    'Query',
]


class Query(BaseModel):
    """Search query."""
    user_uuid: str
    tags_and: list[str]
    tags_or: list[str]
    tags_not: list[str]
    page: int
    items_per_page: int

    def __len__(self) -> int:
        """Return total amount of user tags."""
        return sum((
            len(self.tags_and),
            len(self.tags_or),
            len(self.tags_not),
        ))

    def __repr__(self) -> str:
        """Return textual representation."""
        return f'Query<{len(self)}>'

    def __bool__(self) -> bool:
        """Return True if query has actual tags to search."""
        return any((
            self.tags_and,
            self.tags_or,
            self.tags_not,
        ))
