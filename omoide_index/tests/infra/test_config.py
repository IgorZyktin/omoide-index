# -*- coding: utf-8 -*-

"""Tests.
"""
import os
from datetime import datetime
from datetime import timezone
from unittest import mock

import pytest

from omoide_index.infra import Config


@pytest.fixture
def infra_config_instance():
    return Config()


def test_clock_delta_str(infra_config_instance):
    # arrange
    inst = infra_clock_instance
    before = datetime(2021, 12, 25, 14, 29, 24).replace(tzinfo=timezone.utc)
    after = datetime(2021, 12, 25, 14, 48, 13).replace(tzinfo=timezone.utc)
    ref = '18m 49s'

    # act
    res = inst.delta_str(before, after)

    # assert
    assert res == ref


@pytest.mark.parametrize('value,is_on', [
    ('1', True),
    ('true', True),
    ('True', True),
    ('yes', True),
    ('false', False),
    ('False', False),
    ('no', False),
    ('0', False),
    ('wtf', False),
])
def test_config_is_on(value, is_on):
    # arrange
    inst = Config()

    with mock.patch.dict(os.environ, {'test-var': value}):
        # assert
        assert inst.is_on('test-var') is is_on
