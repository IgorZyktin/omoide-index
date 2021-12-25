# -*- coding: utf-8 -*-
"""Search engine index.
"""

from pydantic import BaseModel

__all__ = [
    'IndexActionModel',
    'IndexRefreshModel',
    'Index',
]


class IndexActionModel(BaseModel):
    """API returns it to describe confirmed actions."""
    action: str


class IndexRefreshModel(BaseModel):
    """Command to refresh components of the index."""
    action: str


class Index(BaseModel):
    """Main information storage."""
