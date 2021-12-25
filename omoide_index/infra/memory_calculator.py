# -*- coding: utf-8 -*-
"""Infrastructure."""
import os
import typing

import psutil
from pympler import asizeof

from omoide_index.domain import infra as domain_infra


class MemoryCalculator(domain_infra.AbstractMemoryCalculator):
    """Memory monitoring tool."""
    SUFFIXES = {
        'RU': {'B': 'Б', 'kB': 'кБ', 'MB': 'МБ', 'GB': 'ГБ', 'TB': 'ТБ',
               'PB': 'ПБ', 'EB': 'ЭБ', 'KiB': 'КиБ', 'MiB': 'МиБ',
               'GiB': 'ГиБ', 'TiB': 'ТиБ', 'PiB': 'ПиБ', 'EiB': 'ЭиБ'},

        'EN': {'B': 'B', 'kB': 'kB', 'MB': 'MB', 'GB': 'GB', 'TB': 'TB',
               'PB': 'PB', 'EB': 'EB', 'KiB': 'KiB', 'MiB': 'MiB',
               'GiB': 'GiB', 'TiB': 'TiB', 'PiB': 'PiB', 'EiB': 'EiB'},
    }

    def __init__(self):
        """Initialize instance."""
        self.process = psutil.Process(os.getpid())

    def get_process_memory_consumption(self) -> int:
        """Return process memory consumption in bytes."""
        return self.process.memory_info()[0]

    def get_process_memory_consumption_str(self) -> str:
        """Return process memory consumption in human readable string."""
        return self.format_human_readable_size(
            total_bytes=self.get_process_memory_consumption(),
        )

    def get_object_memory_consumption(self, target: typing.Any) -> int:
        """Return object memory consumption in bytes."""
        return asizeof.asizeof(target)

    def get_object_memory_consumption_str(self, target: typing.Any) -> str:
        """Return object memory consumption in human readable string."""
        return self.format_human_readable_size(
            total_bytes=self.get_object_memory_consumption(target),
        )

    def format_human_readable_size(self, total_bytes: int,
                                   language: str = 'EN') -> str:
        """Convert amount of bytes into human readable format.

        >>> MemoryCalculator().format_human_readable_size(1023)
        '1023 B'
        """
        total_bytes = float(max(0, total_bytes))

        prefix = ''
        if total_bytes < 0:
            prefix = '-'
            total_bytes = abs(total_bytes)

        if total_bytes < 1024:
            suffix = self.SUFFIXES[language]['B']
            return f'{prefix}{int(total_bytes)} {suffix}'

        total_bytes /= 1024

        if total_bytes < 1024:
            suffix = self.SUFFIXES[language]['KiB']
            return f'{prefix}{total_bytes:0.1f} {suffix}'

        total_bytes /= 1024

        if total_bytes < 1024:
            suffix = self.SUFFIXES[language]['MiB']
            return f'{prefix}{total_bytes:0.1f} {suffix}'

        total_bytes /= 1024

        if total_bytes < 1024:
            suffix = self.SUFFIXES[language]['GiB']
            return f'{prefix}{total_bytes:0.1f} {suffix}'

        total_bytes /= 1024

        if total_bytes < 1024:
            suffix = self.SUFFIXES[language]['TiB']
            return f'{prefix}{total_bytes:0.1f} {suffix}'

        suffix = self.SUFFIXES[language]['EiB']
        return f'{total_bytes / 1024 / 1024 :0.1f} {suffix}'
