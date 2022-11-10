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

"""Test suite for the API functions."""

import os
import pytest

from wordcab import (
    change_speaker_labels,
    delete_job,
    get_stats,
    list_jobs,
    list_summaries,
    list_transcripts,
    request,
    retrieve_job,
    retrieve_summary,
    retrieve_transcript,
    start_extract,
    start_summary,
)
from wordcab.core_objects import Stats


@pytest.fixture
def api_key():
    """Fixture for the API key."""
    return "dummy_api_key"


@pytest.mark.parametrize(
    "method",
    [
        "change_speaker_labels",
        "delete_job",
        "list_jobs",
        "list_summaries",
        "list_transcripts",
        "retrieve_job",
        "retrieve_summary",
        "retrieve_transcript",
        "start_extract",
        "start_summary",
    ],
)
def test_request(api_key: str, method: str) -> None:
    """Test the request function."""
    with pytest.raises(NotImplementedError):
        request(method=method, api_key=api_key)


def test_get_stats() -> None:
    """Test the get_stats function."""
    api_key = os.environ.get("WORDCAB_API_KEY")
    stats = get_stats(api_key=api_key, min_created="2021-01-01", max_created="2021-01-31")
    assert isinstance(stats, Stats)
    assert hasattr(stats, "account_email")
    assert hasattr(stats, "plan")
    assert hasattr(stats, "monthly_request_limit")
    assert hasattr(stats, "request_count")
    assert hasattr(stats, "minutes_summarized")
    assert hasattr(stats, "transcripts_summarized")
    assert hasattr(stats, "metered_charge")
    assert hasattr(stats, "min_created")
    assert stats.min_created == "2021-01-01T00:00:00"
    assert hasattr(stats, "max_created")
    assert stats.max_created == "2021-01-31T00:00:00"
    assert hasattr(stats, "tags")
    assert stats.tags is None


def test_list_jobs(api_key: str) -> None:
    """Test the list_jobs function."""
    with pytest.raises(NotImplementedError):
        list_jobs(api_key=api_key)


def test_list_summaries(api_key: str) -> None:
    """Test the list_summaries function."""
    with pytest.raises(NotImplementedError):
        list_summaries(api_key=api_key)


def test_list_transcripts(api_key: str) -> None:
    """Test the list_transcripts function."""
    with pytest.raises(NotImplementedError):
        list_transcripts(api_key=api_key)


def test_retrieve_job(api_key: str) -> None:
    """Test the retrieve_job function."""
    with pytest.raises(NotImplementedError):
        retrieve_job(api_key=api_key)


def test_retrieve_summary(api_key: str) -> None:
    """Test the retrieve_summary function."""
    with pytest.raises(NotImplementedError):
        retrieve_summary(api_key=api_key)


def test_retrieve_transcript(api_key: str) -> None:
    """Test the retrieve_transcript function."""
    with pytest.raises(NotImplementedError):
        retrieve_transcript(api_key=api_key)


def test_start_extract(api_key: str) -> None:
    """Test the start_extract function."""
    with pytest.raises(NotImplementedError):
        start_extract(api_key=api_key)


def test_start_summary(api_key: str) -> None:
    """Test the start_summary function."""
    with pytest.raises(NotImplementedError):
        start_summary(api_key=api_key)


def test_change_speaker_labels(api_key: str) -> None:
    """Test the change_speaker_labels function."""
    with pytest.raises(NotImplementedError):
        change_speaker_labels(api_key=api_key)


def test_delete_job(api_key: str) -> None:
    """Test the delete_job function."""
    with pytest.raises(NotImplementedError):
        delete_job(api_key=api_key)
