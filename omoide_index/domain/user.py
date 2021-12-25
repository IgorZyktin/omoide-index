# -*- coding: utf-8 -*-
"""User related models.
"""

from pydantic import BaseModel

__all__ = [
    'UserRefreshModel',
    'UserDropModel',
    'UserActionModel',
]


class UserRefreshModel(BaseModel):
    """Comes with command for refresh."""
    user_uuid: str
    refresh_all: bool
    refresh_items: list[str]


class UserDropModel(BaseModel):
    """Comes with command for deletion."""
    user_uuid: str


class UserActionModel(BaseModel):
    """API returns it to describe confirmed actions."""
    user_uuid: str
    action: str
