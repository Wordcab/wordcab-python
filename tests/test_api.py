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
from pathlib import Path
from typing import Optional

import pytest

from wordcab import (
    change_speaker_labels,
    delete_job,
    get_stats,
    list_jobs,
    list_summaries,
    list_transcripts,
    retrieve_job,
    retrieve_summary,
    retrieve_transcript,
    start_extract,
    start_summary,
)
from wordcab.core_objects import (
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
def api_key() -> Optional[str]:
    """Fixture for the API key."""
    return os.environ.get("WORDCAB_API_KEY")


def test_get_stats(api_key: str) -> None:
    """Test the get_stats function."""
    stats = get_stats(
        api_key=api_key, min_created="2021-01-01", max_created="2021-01-31"
    )
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
    jobs = list_jobs(api_key=api_key)
    assert jobs is not None
    assert isinstance(jobs, ListJobs)
    assert jobs.page_count is not None
    assert isinstance(jobs.page_count, int)
    assert jobs.next_page is not None
    assert isinstance(jobs.next_page, str)
    assert jobs.results is not None
    assert isinstance(jobs.results, list)

    with pytest.raises(ValueError):
        list_jobs(order_by="invalid")
    with pytest.raises(ValueError):
        list_jobs(order_by="+time_started")
    with pytest.raises(ValueError):
        list_jobs(order_by="+time_completed")


def test_list_summaries(api_key: str) -> None:
    """Test the list_summaries function."""
    li_summaries = list_summaries(api_key=api_key)
    assert li_summaries is not None
    assert isinstance(li_summaries, ListSummaries)
    assert li_summaries.page_count is not None
    assert isinstance(li_summaries.page_count, int)
    assert li_summaries.next_page is not None
    assert isinstance(li_summaries.next_page, str)
    assert li_summaries.results is not None
    assert isinstance(li_summaries.results, list)
    for summary in li_summaries.results:
        assert isinstance(summary, BaseSummary)
        assert summary.summary_id is not None
        assert summary.job_status is not None


def test_list_transcripts(api_key: str) -> None:
    """Test the list_transcripts function."""
    li_transcripts = list_transcripts(api_key=api_key)
    assert li_transcripts is not None
    assert isinstance(li_transcripts, ListTranscripts)
    assert li_transcripts.page_count is not None
    assert isinstance(li_transcripts.page_count, int)
    assert li_transcripts.next_page is not None
    assert isinstance(li_transcripts.next_page, str)
    assert li_transcripts.results is not None
    assert isinstance(li_transcripts.results, list)
    for transcript in li_transcripts.results:
        assert isinstance(transcript, BaseTranscript)
        assert transcript.transcript_id is not None
        assert isinstance(transcript.transcript_id, str)
        assert transcript.job_id_set is not None
        assert isinstance(transcript.job_id_set, list)
        assert transcript.summary_id_set is not None
        assert isinstance(transcript.summary_id_set, list)


def test_retrieve_job(api_key: str) -> None:
    """Test the retrieve_job function."""
    job = retrieve_job(job_name="job_VkzpZbp79KVv4SoTiW8bFATY4FVQ9rCp", api_key=api_key)
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
    job = retrieve_job(job_name="job_6R9gfLmgkDUjhTLhj2Xq6oW7FEPs736n", api_key=api_key)
    assert job.job_name == "job_6R9gfLmgkDUjhTLhj2Xq6oW7FEPs736n"
    assert job is not None
    assert isinstance(job, ExtractJob)
    assert job.job_status is not None
    assert job.display_name is not None
    assert job.source is not None
    assert job.time_started is not None
    assert job.time_completed is not None
    assert job.transcript_id is not None


def test_retrieve_summary(api_key: str) -> None:
    """Test the retrieve_summary function."""
    summary = retrieve_summary(
        summary_id="narrative_summary_VYJfH4TbBgQx6LHJKXgsPZwG9nRGgh8m", api_key=api_key
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
        assert isinstance(value["structured_summary"][0], StructuredSummary)
        assert value["structured_summary"][0].end is not None
        assert value["structured_summary"][0].start is not None
        assert value["structured_summary"][0].summary is not None
        assert value["structured_summary"][0].summary_html is not None
        assert value["structured_summary"][0].timestamp_end is not None
        assert value["structured_summary"][0].timestamp_start is not None
        assert value["structured_summary"][0].transcript_segment is not None
        assert isinstance(value["structured_summary"][0].transcript_segment, list)
        for segment in value["structured_summary"][0].transcript_segment:
            assert isinstance(segment, dict)
            assert "speaker" in segment
            assert "text" in segment
            assert "timestamp_end" in segment
            assert "timestamp_start" in segment
            assert "start" in segment


def test_retrieve_transcript(api_key: str) -> None:
    """Test the retrieve_transcript function."""
    transcript = retrieve_transcript(
        transcript_id="generic_transcript_JU74t3Tjzahn5DodBLwsDrS2EvGdb4bS",
        api_key=api_key,
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


def test_start_extract(api_key: str) -> None:
    """Test the start_extract function."""
    source_object = GenericSource(filepath=Path("tests/sample_1.txt"))
    job = start_extract(
        source_object=source_object,
        display_name="test-extract-api",
        pipelines=["emotions"],
        api_key=api_key,
    )
    assert isinstance(job, ExtractJob)
    assert job.display_name == "test-extract-api"
    assert job.job_name is not None
    assert job.source == "generic"
    assert job.settings == JobSettings(
        ephemeral_data=False,
        pipeline="emotions",
        split_long_utterances=False,
        only_api=True,
    )


def test_start_summary(api_key: str) -> None:
    """Test the start_summary function."""
    source_object = GenericSource(filepath=Path("tests/sample_1.txt"))
    job = start_summary(
        source_object=source_object,
        display_name="test-summary-api",
        summary_type="conversational",
        api_key=api_key,
    )
    assert isinstance(job, SummarizeJob)
    assert job.display_name == "test-summary-api"
    assert job.job_name is not None
    assert job.source == "generic"
    assert job.settings == JobSettings(
        ephemeral_data=False,
        pipeline="transcribe,summarize",
        split_long_utterances=False,
        only_api=True,
    )


def test_change_speaker_labels(api_key: str) -> None:
    """Test the change_speaker_labels function."""
    transcript = change_speaker_labels(
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


def test_delete_job(api_key: str) -> None:
    """Test the delete_job function."""
    deleted_job = delete_job(
        job_name="job_aLt5gw5AZwg2rnqaqR46kB7csMfwqTdB", api_key=api_key
    )
    assert deleted_job is not None
    assert isinstance(deleted_job, dict)
    assert deleted_job["job_name"] == "job_aLt5gw5AZwg2rnqaqR46kB7csMfwqTdB"
