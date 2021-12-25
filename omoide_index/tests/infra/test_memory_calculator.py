# -*- coding: utf-8 -*-

"""Tests.
"""

import pytest

from omoide_index.infra import MemoryCalculator


@pytest.fixture
def infra_memory_calculator_instance():
    return MemoryCalculator()


def test_memory_calculator_consumption_str(infra_memory_calculator_instance):
    # arrange
    inst = infra_memory_calculator_instance

    # act
    res = inst.get_process_memory_consumption_str()

    # assert
    assert res.endswith('MiB')


@pytest.mark.parametrize('size,string', [
    (-1, '0 B'),
    (0, '0 B'),
    (5, '5 B'),
    (29, '29 B'),
    (60, '60 B'),
    (1_000, '1000 B'),
    (1_024, '1.0 KiB'),
    (1_120, '1.1 KiB'),
    (99_999, '97.7 KiB'),
    (98_962_693, '94.4 MiB'),
    (100_000_000_000, '93.1 GiB'),
    (100_000_000_000_000, '90.9 TiB'),
])
def test_memory_calculator_human_readable_size(size, string):
    # arrange
    inst = MemoryCalculator()

    # assert
    assert inst.format_human_readable_size(size) == string


@pytest.mark.parametrize('target,string', [
    (True, '32 B'),
    (False, '24 B'),
    (None, '16 B'),
    (1, '32 B'),
    ((1, 2, 3), '160 B'),
    ((1, 2, (3, 4, (5, 6))), '376 B'),
])
def test_memory_calculator_object_consumption(target, string):
    # arrange
    inst = MemoryCalculator()

    # assert
    assert inst.get_object_memory_consumption_str(target) == string
