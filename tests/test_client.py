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

"""Test suite for the Wordcab Client."""

import logging
import os
from pathlib import Path

import pytest

from wordcab import Client
from wordcab.core_objects import BaseSource, GenericSource, JobSettings, Stats, SummarizeJob


@pytest.fixture
def client() -> Client:
    """Fixture for a Wordcab Client object."""
    return Client(api_key="dummy_api_key")


@pytest.fixture
def generic_source() -> GenericSource:
    """Fixture for a GenericSource object."""
    return GenericSource(
        filepath=Path("tests/sample_1.txt")
    )


@pytest.fixture
def base_source() -> BaseSource:
    """Fixture for a wrong BaseSource object."""
    return BaseSource(
        filepath=Path("tests/sample_1.txt")
    )


def test_client_succeeds(client: Client) -> None:
    """Test client."""
    assert client.api_key == "dummy_api_key"


def test_client_enter_exit(client: Client) -> None:
    """Test client enter and exit methods."""
    with Client(api_key="dummy_api_key") as client:
        assert client.api_key == "dummy_api_key"


def test_request(client: Client) -> None:
    """Test client request method."""
    with pytest.raises(ValueError):
        client.request(method=None)


def test_get_stats() -> None:
    """Test client get_stats method."""
    api_key = os.environ.get("WORDCAB_API_KEY")
    with Client(api_key=api_key) as client:
        stats = client.get_stats(min_created="2021-01-01", max_created="2021-01-31")
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


def test_start_extract(client: Client) -> None:
    """Test client start_extract method."""
    with pytest.raises(NotImplementedError):
        client.start_extract()


def test_start_summary(
    base_source: BaseSource, generic_source: GenericSource, caplog: pytest.LogCaptureFixture
) -> None:
    """Test client start_summary method."""
    api_key = os.environ.get("WORDCAB_API_KEY")
    with Client(api_key=api_key) as client:
        with pytest.raises(ValueError):
            client.start_summary(source_object=generic_source, display_name="test")
        with pytest.raises(ValueError):
            client.start_summary(source_object=generic_source, display_name="test", summary_type="invalid")
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=generic_source, display_name="test", summary_type="reason_conclusion", summary_length=0
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=generic_source,
                display_name="test",
                summary_type="narrative",
                summary_length=3,
                pipelines=["invalid"],
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object={"invalid": "invalid"},
                display_name="test",
                summary_type="narrative",
                summary_length=3,
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=base_source,
                display_name="test",
                summary_type="narrative",
                summary_length=3,
            )
        with pytest.raises(ValueError):
            base_source.source = "generic"
            client.start_summary(
                source_object=base_source,
                display_name="test",
                summary_type="narrative",
                summary_length=3,
            )
        with caplog.at_level(logging.WARNING):
            job = client.start_summary(
                source_object=generic_source,
                display_name="test",
                summary_type="reason_conclusion",
                summary_length=3,
            )
            assert (
                """
                You have specified a summary length for a reason_conclusion summary but reason_conclusion summaries
                do not use a summary length. The summary_length parameter will be ignored.
                """
                in caplog.text
            )
            assert isinstance(job, SummarizeJob)
            assert job.display_name == "test"
            assert job.job_name is not None
            assert job.source == "generic"
            assert job.settings == JobSettings(
                ephemeral_data=False,
                pipeline=["transcribe", "summarize"],
                split_long_utterances=False,
                only_api=True,
            )
    

def test_list_jobs(client: Client) -> None:
    """Test client list_jobs method."""
    with pytest.raises(NotImplementedError):
        client.list_jobs()


def test_retrieve_job(client: Client) -> None:
    """Test client retrieve_job method."""
    with pytest.raises(NotImplementedError):
        client.retrieve_job()


def test_delete_job(client: Client) -> None:
    """Test client delete_job method."""
    with pytest.raises(NotImplementedError):
        client.delete_job()


def test_list_transcripts(client: Client) -> None:
    """Test client list_transcripts method."""
    with pytest.raises(NotImplementedError):
        client.list_transcripts()


def test_retrieve_transcript(client: Client) -> None:
    """Test client retrieve_transcript method."""
    with pytest.raises(NotImplementedError):
        client.retrieve_transcript()


def test_change_speaker_labels(client: Client) -> None:
    """Test client change_speaker_labels method."""
    with pytest.raises(NotImplementedError):
        client.change_speaker_labels()


def test_list_summaries(client: Client) -> None:
    """Test client list_summaries method."""
    with pytest.raises(NotImplementedError):
        client.list_summaries()


def test_retrieve_summary(client: Client) -> None:
    """Test client retrieve_summary method."""
    with pytest.raises(NotImplementedError):
        client.retrieve_summary()
