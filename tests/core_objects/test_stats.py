# Copyright 2022 The Wordcab Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test suite for the stats dataclass."""

import logging
from typing import List

import pytest

from wordcab.core_objects import Stats


logger = logging.getLogger(__name__)


@pytest.fixture
def dummy_stats() -> Stats:
    """Fixture for a dummy Stats object."""
    return Stats(
        account_email="azerty@gmail.com",
        plan="free",
        monthly_request_limit="1000",
        request_count=0,
        minutes_summarized=0,
        transcripts_summarized=0,
        metered_charge="$0",
        min_created="2021-01-01",
        max_created="2021-02-01",
    )


def test_stats_init(dummy_stats: Stats) -> None:
    """Test the Stats object init."""
    assert dummy_stats.account_email == "azerty@gmail.com"
    assert dummy_stats.plan == "free"
    assert dummy_stats.monthly_request_limit == "1000"
    assert dummy_stats.request_count == 0
    assert dummy_stats.minutes_summarized == 0
    assert dummy_stats.transcripts_summarized == 0
    assert dummy_stats.metered_charge == "$0"
    assert dummy_stats.min_created == "2021-01-01"
    assert dummy_stats.max_created == "2021-02-01"
    assert dummy_stats.tags == []


@pytest.mark.parametrize("plan", ["professional", "freeee", "proffessional"])
def test_stats_init_wrong_plan(plan: str) -> None:
    """Test the Stats object init with wrong plan."""
    with pytest.raises(ValueError):
        Stats(
            account_email="azerty@gmail.com",
            plan=plan,
            monthly_request_limit="1000",
            request_count=0,
            minutes_summarized=0,
            transcripts_summarized=0,
            metered_charge="$0",
            min_created="2021-01-01",
            max_created="2021-02-01",
        )


@pytest.mark.parametrize("metered_charge", ["0.0", "0", "A.B", "A", "$A", "$A.B"])
def test_stats_init_wrong_metered_charge(metered_charge: str) -> None:
    """Test the Stats object init with wrong metered charge."""
    with pytest.raises(ValueError):
        Stats(
            account_email="azerty@gmail.com",
            plan="free",
            monthly_request_limit="1000",
            request_count=0,
            minutes_summarized=0,
            transcripts_summarized=0,
            metered_charge=metered_charge,
            min_created="2021-01-01",
            max_created="2021-02-01",
        )


@pytest.mark.parametrize("timestamps", ["2021-02-01", "2021-01-01"])
def test_stats_init_wrong_timestamps(timestamps: List[str]) -> None:
    """Test the Stats object init with wrong timestamps."""
    with pytest.raises(ValueError):
        Stats(
            account_email="azerty@gmail.com",
            plan="free",
            monthly_request_limit="1000",
            request_count=0,
            minutes_summarized=0,
            transcripts_summarized=0,
            metered_charge="$0",
            min_created=timestamps[0],
            max_created=timestamps[1],
        )


@pytest.mark.parametrize("email", ["azerty", "azerty@", "azerty@gmail", ""])
def test_stats_init_wrong_email(email: str) -> None:
    """Test the Stats object init with wrong email."""
    with pytest.raises(ValueError):
        Stats(
            account_email=email,
            plan="free",
            monthly_request_limit="1000",
            request_count=0,
            minutes_summarized=0,
            transcripts_summarized=0,
            metered_charge="$0",
            min_created="2021-01-01",
            max_created="2021-02-01",
        )
