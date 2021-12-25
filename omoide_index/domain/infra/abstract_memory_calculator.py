# -*- coding: utf-8 -*-
"""Base class for memory getter."""
import abc


class AbstractMemoryCalculator(abc.ABC):
    """Base class for memory getter."""

    @abc.abstractmethod
    def get_process_memory_consumption(self) -> int:
        """Return total memory consumption in bytes."""

    @abc.abstractmethod
    def get_process_memory_consumption_str(self) -> int:
        """Return total memory consumption in human readable string."""

    @abc.abstractmethod
    def format_human_readable_size(self, total_bytes: int) -> str:
        """Return object size in human readable string."""
