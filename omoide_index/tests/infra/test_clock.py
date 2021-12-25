# -*- coding: utf-8 -*-

"""Tests.
"""
from datetime import datetime
from datetime import timezone
from unittest import mock

import pytest

from omoide_index.infra import Clock


@pytest.fixture
def infra_clock_instance():
    return Clock()


def test_clock_now_str(infra_clock_instance):
    # arrange
    inst = infra_clock_instance
    ref = datetime(2021, 12, 25, 14, 29).replace(tzinfo=timezone.utc)
    ref_str = '2021-12-25 14:29:00+00:00'

    # act
    with mock.patch('omoide_index.infra.clock.datetime') as fake_datetime:
        fake_datetime.utcnow.return_value = ref
        res = inst.now_str()

    # assert
    assert res == ref_str


def test_clock_delta_str(infra_clock_instance):
    # arrange
    inst = infra_clock_instance
    before = datetime(2021, 12, 25, 14, 29, 24).replace(tzinfo=timezone.utc)
    after = datetime(2021, 12, 25, 14, 48, 13).replace(tzinfo=timezone.utc)
    ref = '18m 49s'

    # act
    res = inst.delta_str(before, after)

    # assert
    assert res == ref


@pytest.mark.parametrize('duration,string', [
    (-10, '0s'),
    (-1, '0s'),
    (0, '0s'),
    (5, '5s'),
    (29, '29s'),
    (60, '1m'),
    (61, '1m 1s'),
    (1_120, '18m 40s'),
    (98_962_693, '163w 4d 9h 38m 13s'),
])
def test_clock_human_readable_duration(duration, string):
    # arrange
    inst = Clock()

    # assert
    assert inst.format_human_readable_duration(duration) == string
