# -*- coding: utf-8 -*-
"""Server status.
"""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

__all__ = [
    'STATUS_INIT',
    'STATUS_ACTIVE',
    'STATUS_RELOADING',
    'STATUS_FAILED',
    'Status',
    'VerboseStatus',
]

STATUS_INIT = 'init'
STATUS_ACTIVE = 'active'
STATUS_RELOADING = 'reloading'
STATUS_FAILED = 'failed'


class Status(BaseModel):
    """Server status."""
    version: str
    server_restart: datetime
    index_status: Literal['init', 'active', 'reloading', 'failed']
    index_reload: datetime
    index_duration: int
    index_traceback: str
    index_records: int
    index_buckets: int
    index_avg_bucket: float
    index_min_bucket: int
    index_max_bucket: int
    index_memory: int
    users: int


class VerboseStatus(BaseModel):
    """Human readable server status."""
    version: str
    server_restart: str
    server_uptime: str
    server_memory: str
    index_status: Literal['init', 'active', 'reloading', 'failed']
    index_reload: str
    index_uptime: str
    index_duration: str
    index_traceback: str
    index_records: int
    index_buckets: int
    index_avg_bucket: float
    index_min_bucket: int
    index_max_bucket: int
    index_memory: str
    users: int
