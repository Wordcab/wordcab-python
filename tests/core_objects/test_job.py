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

"""Test suite for the job dataclasses."""

import logging
from typing import Union

import pytest

from wordcab.config import EXTRACT_AVAILABLE_STATUS, SUMMARIZE_AVAILABLE_STATUS
from wordcab.core_objects import BaseJob, ExtractJob, JobSettings, ListJobs, SummarizeJob


@pytest.fixture
def dummy_job() -> BaseJob:
    """Fixture for a dummy Job object."""
    return BaseJob(
        display_name="Dummy Job",
        job_name="dummy_job",
        settings=JobSettings(),
        source="generic",
        time_started="dummy_time",
        transcript_id="dummy_transcript",
    )


@pytest.fixture
def dummy_extract_job() -> ExtractJob:
    """Fixture for a dummy ExtractJob object."""
    return ExtractJob(
        display_name="Dummy Extract Job",
        job_name="dummy_extract_job",
        settings=JobSettings(),
        source="generic",
        time_started="dummy_time",
        transcript_id="dummy_transcript",
    )


@pytest.fixture
def dummy_summarize_job() -> SummarizeJob:
    """Fixture for a dummy SummarizeJob object."""
    return SummarizeJob(
        display_name="Dummy Summarize Job",
        job_name="dummy_summarize_job",
        settings=JobSettings(),
        source="generic",
        time_started="dummy_time",
        transcript_id="dummy_transcript",
    )


@pytest.fixture
def empty_job_settings() -> JobSettings:
    """Fixture for an empty JobSettings object."""
    return JobSettings()


@pytest.fixture
def dummy_list_jobs() -> ListJobs:
    """Fixture for a dummy ListJobs object."""
    return ListJobs(page_count=3, next_page="https://next_page.com", results=[])


def test_available_status() -> None:
    """Test for the available_status property."""
    assert EXTRACT_AVAILABLE_STATUS == [
        "Deleted",
        "Error",
        "Extracting",
        "ExtractionComplete",
        "ItemQueued",
        "Pending",
        "PreparingExtraction",
    ]
    assert SUMMARIZE_AVAILABLE_STATUS == [
        "Deleted",
        "Error",
        "ItemQueued",
        "Pending",
        "PreparingSummary",
        "PreparingTranscript",
        "Summarizing",
        "SummaryComplete",
        "Transcribing",
        "TranscriptComplete",
    ]


def test_dummy_job(dummy_job: BaseJob) -> None:
    """Test for a dummy Job object."""
    assert dummy_job is not None
    assert dummy_job.display_name == "Dummy Job"
    assert dummy_job.job_name == "dummy_job"
    assert dummy_job.job_status == "Pending"
    assert dummy_job.settings is not None
    assert dummy_job.source == "generic"
    assert dummy_job.time_started == "dummy_time"
    assert dummy_job.time_completed is None
    assert dummy_job.transcript_id == "dummy_transcript"
    assert hasattr(dummy_job, "job_update") and callable(dummy_job.job_update)


def test_job_update(dummy_job: BaseJob, caplog: pytest.LogCaptureFixture) -> None:
    """Test for the job_update method."""
    assert dummy_job.job_update is not None
    assert callable(dummy_job.job_update)
    with caplog.at_level(logging.INFO):
        dummy_job.job_update(parameters={"source": "dummy_source"})
        assert dummy_job.source == "dummy_source"
        assert "Job dummy_job updated: source = dummy_source" in caplog.text
    with caplog.at_level(logging.INFO):
        before_status = dummy_job.job_status
        assert before_status == "Pending"
        dummy_job.job_update(parameters={"job_status": "Pending"})
        assert dummy_job.job_status == before_status
        assert "Job dummy_job not updated: job_status = Pending" in caplog.text
    with caplog.at_level(logging.WARNING):
        dummy_job.job_update(parameters={"new_jobsssss": "coder"})
        assert (
            "Cannot update new_jobsssss in dummy_job, not a valid attribute."
            in caplog.text
        )


def test_dummy_extract_job(dummy_extract_job: ExtractJob) -> None:
    """Test for a dummy ExtractJob object."""
    assert dummy_extract_job is not None
    assert dummy_extract_job.display_name == "Dummy Extract Job"
    assert dummy_extract_job.job_name == "dummy_extract_job"
    assert dummy_extract_job.job_status == "Pending"
    assert dummy_extract_job.settings is not None
    assert dummy_extract_job.source == "generic"
    assert dummy_extract_job.time_started == "dummy_time"
    assert dummy_extract_job.time_completed is None
    assert dummy_extract_job.transcript_id == "dummy_transcript"
    assert dummy_extract_job._job_type == "ExtractJob"
    assert dummy_extract_job.available_status is not None
    assert dummy_extract_job.available_status == EXTRACT_AVAILABLE_STATUS
    assert hasattr(dummy_extract_job, "job_update") and callable(
        dummy_extract_job.job_update
    )


def test_dummy_summarize_job(dummy_summarize_job: SummarizeJob) -> None:
    """Test for a dummy SummarizeJob object."""
    assert dummy_summarize_job is not None
    assert dummy_summarize_job.display_name == "Dummy Summarize Job"
    assert dummy_summarize_job.job_name == "dummy_summarize_job"
    assert dummy_summarize_job.job_status == "Pending"
    assert dummy_summarize_job.settings is not None
    assert dummy_summarize_job.source == "generic"
    assert dummy_summarize_job.time_started == "dummy_time"
    assert dummy_summarize_job.time_completed is None
    assert dummy_summarize_job.transcript_id == "dummy_transcript"
    assert dummy_summarize_job._job_type == "SummarizeJob"
    assert dummy_summarize_job.summary_details is None
    assert dummy_summarize_job.available_status is not None
    assert dummy_summarize_job.available_status == SUMMARIZE_AVAILABLE_STATUS
    assert hasattr(dummy_summarize_job, "job_update") and callable(
        dummy_summarize_job.job_update
    )


@pytest.mark.parametrize("source", ["youtube", 123, ""])
def test_wrong_job_source(source: Union[str, int]) -> None:
    """Test for a wrong job source."""
    with pytest.raises(ValueError):
        BaseJob(
            display_name="Dummy Job",
            job_name="dummy_job",
            source=source,
            settings=JobSettings(),
        )
    with pytest.raises(ValueError):
        ExtractJob(
            display_name="Dummy Extract Job",
            job_name="dummy_extract_job",
            source=source,
            settings=JobSettings(),
        )
    with pytest.raises(ValueError):
        SummarizeJob(
            display_name="Dummy Summarize Job",
            job_name="dummy_summarize_job",
            source=source,
            settings=JobSettings(),
        )


def test_empty_job_settings(empty_job_settings: JobSettings) -> None:
    """Test for an empty JobSettings object."""
    assert empty_job_settings is not None
    assert empty_job_settings.ephemeral_data is False
    assert empty_job_settings.pipeline is None
    assert empty_job_settings.only_api is True
    assert empty_job_settings.split_long_utterances is False


def test_list_jobs(dummy_list_jobs: ListJobs) -> None:
    """Test for the list_jobs method."""
    assert dummy_list_jobs is not None
    assert dummy_list_jobs.page_count == 3
    assert dummy_list_jobs.next_page == "https://next_page.com"
    assert dummy_list_jobs.results == []
