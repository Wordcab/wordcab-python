# coding=utf-8
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

import pytest

from wordcab.core_objects import Job, JobSettings


@pytest.fixture
def dummy_job() -> Job:
    """Fixture for a dummy Job object."""
    return Job(display_name="Dummy Job", job_name="dummy_job")


@pytest.fixture
def empty_job_settings() -> JobSettings:
    """Fixture for an empty JobSettings object."""
    return JobSettings()


def test_dummy_job(dummy_job: Job) -> None:
    """Test for a dummy Job object."""
    assert dummy_job is not None
    assert dummy_job.display_name == "Dummy Job"
    assert dummy_job.job_name == "dummy_job"
    assert dummy_job.job_status == "Pending"
    assert dummy_job.settings == {}
    assert dummy_job.settings is not None
    assert dummy_job.source is None
    assert dummy_job.time_started is None
    assert dummy_job.transcript_id is None


def test_empty_job_settings(empty_job_settings: JobSettings) -> None:
    """Test for an empty JobSettings object."""
    assert empty_job_settings is not None
    assert empty_job_settings.ephemeral_data is False
    assert empty_job_settings.pipeline is None
    assert empty_job_settings.only_api is True
    assert empty_job_settings.split_long_utterances is False
