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
from typing import Optional

import pytest

from wordcab import Client
from wordcab.core_objects import (
    AudioSource,
    BaseSource,
    BaseSummary,
    BaseTranscript,
    ExtractJob,
    GenericSource,
    JobSettings,
    ListJobs,
    ListSummaries,
    ListTranscripts,
    Stats,
    StructuredSummary,
    SummarizeJob,
    TranscriptUtterance,
)


@pytest.fixture
def client() -> Client:
    """Client fixture."""
    return Client(api_key="dummy_api_key")


@pytest.fixture
def api_key() -> Optional[str]:
    """Fixture for a valid API key."""
    return os.environ.get("WORDCAB_API_KEY")


@pytest.fixture
def generic_source_txt() -> GenericSource:
    """Fixture for a GenericSource object."""
    return GenericSource(filepath=Path("tests/sample_1.txt"))


@pytest.fixture
def generic_source_json() -> GenericSource:
    """Fixture for a GenericSource object."""
    return GenericSource(filepath=Path("tests/sample_1.json"))


@pytest.fixture
def audio_source() -> AudioSource:
    """Fixture for an AudioSource object."""
    return AudioSource(filepath=Path("tests/sample_1.mp3"))


@pytest.fixture
def base_source() -> BaseSource:
    """Fixture for a wrong BaseSource object."""
    return BaseSource(filepath=Path("tests/sample_1.txt"))


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


def test_get_stats(api_key: str) -> None:
    """Test client get_stats method."""
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


def test_start_extract(
    base_source: BaseSource,
    generic_source_txt: GenericSource,
    generic_source_json: GenericSource,
    audio_source: AudioSource,
    api_key: str,
) -> None:
    """Test client start_extract method."""
    with Client(api_key=api_key) as client:
        with pytest.raises(ValueError):
            client.start_extract(
                source_object=base_source, display_name="test-extraction"
            )
        with pytest.raises(ValueError):
            client.start_extract(
                source_object=generic_source_txt,
                display_name="test-extraction",
                pipelines=["invalid"],
            )
        with pytest.raises(ValueError):
            client.start_extract(source_object={"invalid": "invalid"}, display_name="test-extraction")  # type: ignore
        with pytest.raises(ValueError):
            base_source.source = "generic"
            client.start_extract(
                source_object=base_source, display_name="test-extraction"
            )

        # Test generic source with txt file
        txt_job = client.start_extract(
            source_object=generic_source_txt,
            display_name="test-extraction-txt",
            pipelines=["emotions"],
        )
        assert isinstance(txt_job, ExtractJob)
        assert txt_job.display_name == "test-extraction-txt"
        assert txt_job.job_name is not None
        assert txt_job.source == "generic"
        assert txt_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="emotions",
            split_long_utterances=False,
            only_api=True,
        )

        # Test generic source with json file
        json_job = client.start_extract(
            source_object=generic_source_json,
            display_name="test-extraction-json",
            pipelines=["emotions"],
        )
        assert isinstance(json_job, ExtractJob)
        assert json_job.display_name == "test-extraction-json"
        assert json_job.job_name is not None
        assert json_job.source == "generic"
        assert json_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="emotions",
            split_long_utterances=False,
            only_api=True,
        )

        # # Test audio source
        # audio_job = client.start_extract(
        #     source_object=audio_source, display_name="test-extraction-audio", pipelines=["emotions"]
        # )
        # assert isinstance(audio_job, ExtractJob)
        # assert audio_job.display_name == "test-extraction-audio"
        # assert audio_job.job_name is not None
        # assert audio_job.source == "audio"
        # assert audio_job.settings == JobSettings(
        #     ephemeral_data=False,
        #     pipeline=["emotions"],
        #     split_long_utterances=False,
        #     only_api=True,
        # )


def test_start_summary(
    base_source: BaseSource,
    generic_source_txt: GenericSource,
    generic_source_json: GenericSource,
    audio_source: AudioSource,
    api_key: str,
) -> None:
    """Test client start_summary method."""
    with Client(api_key=api_key) as client:
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=generic_source_txt,
                display_name="test",
                summary_type="invalid",
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=generic_source_txt,
                display_name="test",
                summary_type="reason_conclusion",
                summary_length=0,
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object=generic_source_txt,
                display_name="test",
                summary_type="narrative",
                summary_length=3,
                pipelines=["invalid"],
            )
        with pytest.raises(ValueError):
            client.start_summary(
                source_object={"invalid": "invalid"},  # type: ignore
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

        # Test generic source with txt file
        txt_job = client.start_summary(
            source_object=generic_source_txt,
            display_name="test-sdk-txt",
            summary_type="reason_conclusion",
            summary_length=3,
        )
        assert isinstance(txt_job, SummarizeJob)
        assert txt_job.display_name == "test-sdk-txt"
        assert txt_job.job_name is not None
        assert txt_job.source == "generic"
        assert txt_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )

        # Test generic source with json file
        json_job = client.start_summary(
            source_object=generic_source_json,
            display_name="test-sdk-json",
            summary_type="narrative",
            summary_length=3,
        )
        assert isinstance(json_job, SummarizeJob)
        assert json_job.display_name == "test-sdk-json"
        assert json_job.job_name is not None
        assert json_job.source == "generic"
        assert json_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )

        # Test audio source
        audio_job = client.start_summary(
            source_object=audio_source,
            display_name="test-sdk-audio",
            summary_type="narrative",
            summary_length=3,
        )
        assert isinstance(audio_job, SummarizeJob)
        assert audio_job.display_name == "test-sdk-audio"
        assert audio_job.job_name is not None
        assert audio_job.source == "audio"
        assert audio_job.settings == JobSettings(
            ephemeral_data=False,
            pipeline="transcribe,summarize",
            split_long_utterances=False,
            only_api=True,
        )


def test_list_jobs(api_key: str) -> None:
    """Test client list_jobs method."""
    with Client(api_key=api_key) as client:
        list_jobs = client.list_jobs()
        assert list_jobs is not None
        assert isinstance(list_jobs, ListJobs)
        assert list_jobs.page_count is not None
        assert isinstance(list_jobs.page_count, int)
        assert list_jobs.next_page is not None
        assert isinstance(list_jobs.next_page, str)
        assert list_jobs.results is not None
        assert isinstance(list_jobs.results, list)

        with pytest.raises(ValueError):
            client.list_jobs(order_by="invalid")
        with pytest.raises(ValueError):
            client.list_jobs(order_by="+time_started")
        with pytest.raises(ValueError):
            client.list_jobs(order_by="+time_completed")


def test_retrieve_job(api_key: str) -> None:
    """Test client retrieve_job method."""
    with Client(api_key=api_key) as client:
        # Summarize job
        job = client.retrieve_job(job_name="job_VkzpZbp79KVv4SoTiW8bFATY4FVQ9rCp")
        assert job.job_name == "job_VkzpZbp79KVv4SoTiW8bFATY4FVQ9rCp"
        assert job is not None
        assert isinstance(job, SummarizeJob)
        assert job.job_status is not None
        assert job.display_name is not None
        assert job.source is not None
        assert job.time_started is not None
        assert job.time_completed is not None
        assert job.transcript_id is not None
        assert job.summary_details is not None
        assert isinstance(job.summary_details, dict)

        # Extract job
        job = client.retrieve_job(job_name="job_6R9gfLmgkDUjhTLhj2Xq6oW7FEPs736n")
        assert job.job_name == "job_6R9gfLmgkDUjhTLhj2Xq6oW7FEPs736n"
        assert job is not None
        assert isinstance(job, ExtractJob)
        assert job.job_status is not None
        assert job.display_name is not None
        assert job.source is not None
        assert job.time_started is not None
        assert job.time_completed is not None
        assert job.transcript_id is not None


def test_delete_job(api_key: str) -> None:
    """Test client delete_job method."""
    with Client(api_key=api_key) as client:
        deleted_job = client.delete_job(job_name="job_7WcE9BZ86Ce77esnmHiK7E6vaCLa5P7u")
        assert deleted_job is not None
        assert isinstance(deleted_job, dict)
        assert deleted_job["job_name"] == "job_7WcE9BZ86Ce77esnmHiK7E6vaCLa5P7u"


def test_list_transcripts(api_key: str) -> None:
    """Test client list_transcripts method."""
    with Client(api_key=api_key) as client:
        list_transcripts = client.list_transcripts()
        assert list_transcripts is not None
        assert isinstance(list_transcripts, ListTranscripts)
        assert list_transcripts.page_count is not None
        assert isinstance(list_transcripts.page_count, int)
        assert list_transcripts.next_page is not None
        assert isinstance(list_transcripts.next_page, str)
        assert list_transcripts.results is not None
        assert isinstance(list_transcripts.results, list)
        for transcript in list_transcripts.results:
            assert isinstance(transcript, BaseTranscript)
            assert transcript.transcript_id is not None
            assert isinstance(transcript.transcript_id, str)
            assert transcript.job_id_set is not None
            assert isinstance(transcript.job_id_set, list)
            assert transcript.summary_id_set is not None
            assert isinstance(transcript.summary_id_set, list)


def test_retrieve_transcript(api_key: str) -> None:
    """Test client retrieve_transcript method."""
    with Client(api_key=api_key) as client:
        transcript = client.retrieve_transcript(
            transcript_id="generic_transcript_JU74t3Tjzahn5DodBLwsDrS2EvGdb4bS"
        )
        assert transcript is not None
        assert isinstance(transcript, BaseTranscript)
        assert transcript.transcript_id is not None
        assert isinstance(transcript.transcript_id, str)
        assert transcript.job_id_set is not None
        assert isinstance(transcript.job_id_set, list)
        assert transcript.summary_id_set is not None
        assert isinstance(transcript.summary_id_set, list)
        assert transcript.speaker_map is not None
        assert isinstance(transcript.speaker_map, dict)
        assert transcript.transcript is not None
        assert isinstance(transcript.transcript, list)
        for utterance in transcript.transcript:
            assert isinstance(utterance, TranscriptUtterance)
            assert utterance.end is not None
            assert isinstance(utterance.end, str)
            assert utterance.start is not None
            assert isinstance(utterance.start, str)
            assert utterance.speaker is not None
            assert isinstance(utterance.speaker, str)
            assert utterance.text is not None
            assert isinstance(utterance.text, str)
            assert utterance.timestamp_end is not None
            assert isinstance(utterance.timestamp_end, int)
            assert utterance.timestamp_start is not None
            assert isinstance(utterance.timestamp_start, int)


def test_change_speaker_labels(api_key: str) -> None:
    """Test client change_speaker_labels method."""
    with Client(api_key=api_key) as client:
        transcript = client.change_speaker_labels(
            transcript_id="generic_transcript_JtugR2ELM9u4VSXJmscek7yuKupokH8t",
            speaker_map={"A": "Tom", "B": "Tam", "C": "Tim", "D": "Tum", "E": "Tym"},
        )
        assert transcript is not None
        assert isinstance(transcript, BaseTranscript)
        assert transcript.transcript_id is not None
        assert isinstance(transcript.transcript_id, str)
        assert transcript.job_id_set is not None
        assert isinstance(transcript.job_id_set, list)
        assert transcript.summary_id_set is not None
        assert isinstance(transcript.summary_id_set, list)
        assert transcript.speaker_map is not None
        assert isinstance(transcript.speaker_map, dict)
        assert transcript.speaker_map == {
            "A": "Tom",
            "B": "Tam",
            "C": "Tim",
            "D": "Tum",
            "E": "Tym",
        }
        assert transcript.transcript is not None
        assert isinstance(transcript.transcript, list)


def test_list_summaries(api_key: str) -> None:
    """Test client list_summaries method."""
    with Client(api_key=api_key) as client:
        list_summaries = client.list_summaries()
        assert list_summaries is not None
        assert isinstance(list_summaries, ListSummaries)
        assert list_summaries.page_count is not None
        assert isinstance(list_summaries.page_count, int)
        assert list_summaries.next_page is not None
        assert isinstance(list_summaries.next_page, str)
        assert list_summaries.results is not None
        assert isinstance(list_summaries.results, list)
        for summary in list_summaries.results:
            assert isinstance(summary, BaseSummary)
            assert summary.summary_id is not None
            assert summary.job_status is not None


def test_retrieve_summary(api_key: str) -> None:
    """Test client retrieve_summary method."""
    with Client(api_key=api_key) as client:
        summary = client.retrieve_summary(
            summary_id="narrative_summary_VYJfH4TbBgQx6LHJKXgsPZwG9nRGgh8m"
        )
        assert summary is not None
        assert isinstance(summary, BaseSummary)
        assert summary.summary_id is not None
        assert summary.job_status is not None
        assert summary.job_name is not None
        assert summary.display_name is not None
        assert summary.summary_type is not None
        assert summary.source is not None
        assert summary.speaker_map is not None
        assert summary.time_started is not None
        assert summary.time_completed is not None
        assert isinstance(summary.summary, dict)
        for key, value in summary.summary.items():
            assert isinstance(key, str)
            assert isinstance(value["structured_summary"], StructuredSummary)
            assert value["structured_summary"].end is not None
            assert value["structured_summary"].start is not None
            assert value["structured_summary"].summary is not None
            assert value["structured_summary"].summary_html is not None
            assert value["structured_summary"].timestamp_end is not None
            assert value["structured_summary"].timestamp_start is not None
            assert value["structured_summary"].transcript_segment is not None
            assert isinstance(value["structured_summary"].transcript_segment, list)
            for segment in value["structured_summary"].transcript_segment:
                assert isinstance(segment, dict)
                assert "speaker" in segment
                assert "text" in segment
                assert "timestamp_end" in segment
                assert "timestamp_start" in segment
                assert "start" in segment
