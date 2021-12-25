# -*- coding: utf-8 -*-
"""Infrastructure."""
import abc
from datetime import datetime


class AbstractClock(abc.ABC):
    """Base class for datetime/time management."""

    @abc.abstractmethod
    def now(self) -> datetime:
        """Return current moment in time.

        Timezone is UTC, milliseconds are truncated.

        Example:
            2021-12-25 12:09:00+00:00
        """

    @abc.abstractmethod
    def now_str(self) -> str:
        """Return current moment in time as string.

        Timezone is UTC, milliseconds are truncated.

        Example:
            '2021-12-25 12:09:00+00:00'
        """

    @abc.abstractmethod
    def as_str(self, moment: datetime) -> str:
        """Return given moment in time as string.

        Example:
            2021-12-25 12:09:00+00:00 -> '2021-12-25 12:09:00+00:00'
        """

    @abc.abstractmethod
    def delta_sec(self, before: datetime, after: datetime) -> int:
        """Return difference in time as integer seconds."""

    @abc.abstractmethod
    def format_human_readable_duration(self, seconds: int) -> str:
        """Format duration as human readable string.

        Negative duration is treated as zero.
        """
