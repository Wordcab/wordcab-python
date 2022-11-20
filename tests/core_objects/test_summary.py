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

"""Test suite for the summary dataclasses."""

import logging
from typing import List, Union

import pytest

from wordcab.core_objects import BaseSummary, ListSummaries, StructuredSummary


logger = logging.getLogger(__name__)


@pytest.fixture
def dummy_empty_structured_summary() -> StructuredSummary:
    """Fixture for a dummy StructuredSummary object."""
    return StructuredSummary(
        end="00:06:49",
        start="00:00:00",
        summary="This is a test.",
        summary_html="<p>This is a test.</p>",
        timestamp_end=409000,
        timestamp_start=0,
    )


@pytest.fixture
def dummy_empty_base_summary() -> BaseSummary:
    """Fixture for a dummy BaseSummary object."""
    return BaseSummary(
        summary_id="summary_123456",
        job_status="job_status",
        process_time="00:00:00",
    )


@pytest.fixture
def dummy_full_base_summary() -> BaseSummary:
    """Fixture for a dummy BaseSummary object."""
    return BaseSummary(
        summary_id="summary_123456",
        job_status="job_status",
        process_time="00:00:00",
        display_name="display_name",
        job_name="job_name",
        speaker_map={"A": "The Speaker", "B": "The Other Speaker"},
        source="generic",
        summary={
            "test": {
                "structured_summary": [
                    StructuredSummary("00:00:10", "00:00:00", "test", "test", 10, 0)
                ]
            }
        },
        summary_type="narrative",
        transcript_id="transcript_123456",
        time_started="2021-01-01T00:00:00",
        time_completed="2021-01-01T00:10:00",
    )


@pytest.fixture
def dummy_list_summaries() -> ListSummaries:
    """Fixture for a dummy ListSummaries object."""
    return ListSummaries(page_count=3, next_page="https://next_page.com", results=[])


def test_empty_structured_summary(
    dummy_empty_structured_summary: StructuredSummary,
) -> None:
    """Test the empty StructuredSummary object."""
    assert dummy_empty_structured_summary.end == "00:06:49"
    assert dummy_empty_structured_summary.start == "00:00:00"
    assert dummy_empty_structured_summary.summary == "This is a test."
    assert dummy_empty_structured_summary.summary_html == "<p>This is a test.</p>"
    assert dummy_empty_structured_summary.timestamp_end == 409000
    assert dummy_empty_structured_summary.timestamp_start == 0
    assert dummy_empty_structured_summary.transcript_segment == []
    assert hasattr(dummy_empty_structured_summary, "_convert_timestamp")
    assert callable(dummy_empty_structured_summary._convert_timestamp)


@pytest.mark.parametrize(
    "params",
    [
        [
            "00:06:49",
            "00:00:00",
            "This is a test.",
            "<p>This is a test.</p>",
            409000,
            409001,
        ],
        [
            "00:06:49",
            "00:00:00",
            "This is a test.",
            "<p>This is a test.</p>",
            409001,
            0,
        ],
        ["00:06:49", "000000", "This is a test.", "<p>This is a test.</p>", 409000, 0],
        ["000649", "00:00:00", "This is a test.", "<p>This is a test.</p>", 409000, 0],
        [405, "00:00:00", "This is a test.", "<p>This is a test.</p>", 409000, 0],
        ["00:06:49", 0, "This is a test.", "<p>This is a test.</p>", 409000, 0],
        [
            "00:06:49",
            "00:00:00",
            ["This is a test."],
            "<p>This is a test.</p>",
            409000,
            0,
        ],
        [
            "00:06:49",
            "00:00:00",
            "This is a test.",
            ["<p>This is a test.</p>"],
            409000,
            0,
        ],
        [
            "00:06:49",
            "00:00:00",
            "This is a test.",
            "<p>This is a test.</p>",
            409000.25,
            0,
        ],
        [
            "00:06:49",
            "00:00:00",
            "This is a test.",
            "<p>This is a test.</p>",
            409000,
            0.0,
        ],
    ],
)
def test_typerror_structured_summary(params: List[Union[str, int, float]]) -> None:
    """Test the wrong StructuredSummary object."""
    with pytest.raises((TypeError, ValueError)):
        StructuredSummary(
            end=params[0],  # type: ignore
            start=params[1],  # type: ignore
            summary=params[2],  # type: ignore
            summary_html=params[3],  # type: ignore
            timestamp_end=params[4],  # type: ignore
            timestamp_start=params[5],  # type: ignore
        )


def test_empty_base_summary(dummy_empty_base_summary: BaseSummary) -> None:
    """Test the empty BaseSummary object."""
    assert dummy_empty_base_summary.summary_id == "summary_123456"
    assert dummy_empty_base_summary.job_status == "job_status"
    assert dummy_empty_base_summary.process_time == "00:00:00"
    assert dummy_empty_base_summary.display_name is None
    assert dummy_empty_base_summary.job_name is None
    assert dummy_empty_base_summary.speaker_map is None
    assert dummy_empty_base_summary.source is None
    assert dummy_empty_base_summary.summary is None
    assert dummy_empty_base_summary.summary_type is None
    assert dummy_empty_base_summary.transcript_id is None
    assert dummy_empty_base_summary.time_started is None
    assert dummy_empty_base_summary.time_completed is None


def test_full_base_summary(dummy_full_base_summary: BaseSummary) -> None:
    """Test the full BaseSummary object."""
    assert dummy_full_base_summary.summary_id == "summary_123456"
    assert dummy_full_base_summary.job_status == "job_status"
    assert dummy_full_base_summary.process_time == "00:00:00"
    assert dummy_full_base_summary.display_name == "display_name"
    assert dummy_full_base_summary.job_name == "job_name"
    assert dummy_full_base_summary.speaker_map == {
        "A": "The Speaker",
        "B": "The Other Speaker",
    }
    assert dummy_full_base_summary.source == "generic"
    assert dummy_full_base_summary.summary == {
        "test": {
            "structured_summary": [
                StructuredSummary("00:00:10", "00:00:00", "test", "test", 10, 0)
            ]
        }
    }
    assert dummy_full_base_summary.summary_type == "narrative"
    assert dummy_full_base_summary.transcript_id == "transcript_123456"
    assert dummy_full_base_summary.time_started == "2021-01-01T00:00:00"
    assert dummy_full_base_summary.time_completed == "2021-01-01T00:10:00"


@pytest.mark.parametrize(
    "params",
    [
        [
            "summary_123456",
            "job_status",
            "narrative",
            "2021-01-01T00:00:00",
            "2021-01-01T00:00:00",
        ],
        [
            "summary_123456",
            "job_status",
            "new_summary_type",
            "2021-01-01T00:00:00",
            "2021-01-01T00:10:00",
        ],
    ],
)
def test_valuerror_base_summary(params: List[str]) -> None:
    """Test the wrong BaseSummary object."""
    with pytest.raises(ValueError):
        BaseSummary(
            summary_id=params[0],
            job_status=params[1],
            summary_type=params[2],
            time_started=params[3],
            time_completed=params[4],
        )


def test_list_summaries(dummy_list_summaries: ListSummaries) -> None:
    """Test the ListSummaries object."""
    assert dummy_list_summaries is not None
    assert dummy_list_summaries.page_count == 3
    assert dummy_list_summaries.next_page == "https://next_page.com"
    assert dummy_list_summaries.results == []
