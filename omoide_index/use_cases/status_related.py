# -*- coding: utf-8 -*-
"""Server related use cases.
"""

from omoide_index import domain
from omoide_index.domain import infra as domain_infra

__all__ = [
    'CreateStatusOnStartUseCase',
    'DescribeExistingStatusUseCase',
]


class CreateStatusOnStartUseCase:
    """When server is started and no status exists at the moment."""

    def __init__(
            self,
            index: domain.Index,
            clock: domain_infra.AbstractClock,
            memory_calculator: domain_infra.AbstractMemoryCalculator,
            version: str,
    ) -> None:
        """Initialize instance."""
        self.index = index
        self.clock = clock
        self.memory_calculator = memory_calculator
        self.version = version

    def execute(self) -> domain.Status:
        """Execute use case."""
        return domain.Status(
            version=self.version,
            server_restart=self.clock.now(),
            index_status=domain.STATUS_INIT,
            index_reload=self.clock.now(),
            index_duration=0,
            index_traceback='',
            index_records=0,
            index_buckets=0,
            index_avg_bucket=0.0,
            index_min_bucket=0,
            index_max_bucket=0,
            index_memory=self.memory_calculator.get_object_memory_consumption(
                target=self.index,
            ),
            users=0,
        )


class DescribeExistingStatusUseCase:
    """When user wants to know is server okay after some work."""

    def __init__(
            self,
            status: domain.Status,
            clock: domain_infra.AbstractClock,
            memory_calculator: domain_infra.AbstractMemoryCalculator,
    ) -> None:
        """Initialize instance."""
        self.status = status
        self.clock = clock
        self.memory_calculator = memory_calculator

    def execute(self) -> domain.VerboseStatus:
        """Execute use case."""
        server_uptime = self.clock.delta_str(
            before=self.status.server_restart,
            after=self.clock.now(),
        )

        index_uptime = self.clock.delta_str(
            before=self.status.index_reload,
            after=self.clock.now(),
        )

        server_memory = self.memory_calculator \
            .get_process_memory_consumption_str()

        index_memory = self.memory_calculator.format_human_readable_size(
            total_bytes=self.status.index_memory,
        )

        index_duration = self.clock.format_human_readable_duration(
            seconds=self.status.index_duration,
        )

        return domain.VerboseStatus(
            version=self.status.version,
            server_restart=self.clock.as_str(self.status.server_restart),
            server_uptime=server_uptime,
            server_memory=server_memory,
            index_status=self.status.index_status,
            index_reload=self.clock.as_str(self.status.index_reload),
            index_duration=index_duration,
            index_uptime=index_uptime,
            index_traceback=self.status.index_traceback,
            index_records=self.status.index_records,
            index_buckets=self.status.index_buckets,
            index_avg_bucket=self.status.index_avg_bucket,
            index_min_bucket=self.status.index_min_bucket,
            index_max_bucket=self.status.index_max_bucket,
            index_memory=index_memory,
            users=self.status.users,
        )
