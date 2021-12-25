# -*- coding: utf-8 -*-
"""Infrastructure."""
from datetime import datetime
from datetime import timezone

from omoide_index.domain import infra as domain_infra


class Clock(domain_infra.AbstractClock):
    """Datetime/time management."""

    def now(self) -> datetime:
        """Return current moment in time.

        Timezone is UTC, milliseconds are truncated.

        Example:
            2021-12-25 12:09:00+00:00
        """
        return datetime.utcnow().replace(
            microsecond=0,
            tzinfo=timezone.utc,
        )

    def now_str(self) -> str:
        """Return current moment in time as string.

        Timezone is UTC, milliseconds are truncated.

        Example:
            '2021-12-25 12:09:00+00:00'
        """
        return self.as_str(self.now())

    def as_str(self, moment: datetime) -> str:
        """Return given moment in time as string.

        Example:
            2021-12-25 12:09:00+00:00 -> '2021-12-25 12:09:00+00:00'
        """
        return str(moment)

    def delta_sec(self, before: datetime, after: datetime) -> int:
        """Return difference in time as integer seconds."""
        return int((after - before).total_seconds())

    def format_human_readable_duration(self, seconds: int) -> str:
        """Format interval as human readable description.

        Negative duration is treated as zero.

        >>> Clock().format_human_readable_duration(46551387)
        '76w 6d 18h 56m 27s'

        >>> Clock().format_human_readable_duration(600)
        '10m'
        """
        if seconds < 1:
            return '0s'

        _suffixes = ('w', 'd', 'h', 'm', 's')

        _minutes, _seconds = divmod(seconds, 60)
        _hours, _minutes = divmod(_minutes, 60)
        _days, _hours = divmod(_hours, 24)
        _weeks, _days = divmod(_days, 7)

        values = [_weeks, _days, _hours, _minutes, _seconds]
        string = ' '.join(
            f'{x}{_suffixes[i]}' for i, x in enumerate(values) if x
        )

        return string
