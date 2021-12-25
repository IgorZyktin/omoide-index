# -*- coding: utf-8 -*-
"""Base class for memory getter."""
import abc
import typing


class AbstractMemoryCalculator(abc.ABC):
    """Base class for memory getter."""

    @abc.abstractmethod
    def get_process_memory_consumption(self) -> int:
        """Return process memory consumption in bytes."""

    @abc.abstractmethod
    def get_process_memory_consumption_str(self) -> int:
        """Return process memory consumption in human readable string."""

    @abc.abstractmethod
    def get_object_memory_consumption(self, target: typing.Any) -> int:
        """Return object memory consumption in bytes."""

    @abc.abstractmethod
    def get_object_memory_consumption_str(self, target: typing.Any) -> str:
        """Return object memory consumption in human readable string."""

    @abc.abstractmethod
    def format_human_readable_size(self, total_bytes: int) -> str:
        """Return given size in bytes as human readable string."""
