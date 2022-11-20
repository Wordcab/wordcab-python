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

"""Test suite for the transcript dataclasses."""

import logging
from typing import Dict, List, Union

import pytest

from wordcab.core_objects import BaseTranscript, ListTranscripts, TranscriptUtterance


logger = logging.getLogger(__name__)


@pytest.fixture
def dummy_transcript_utterance() -> TranscriptUtterance:
    """Fixture for a dummy TranscriptUtterance object."""
    return TranscriptUtterance(
        text="This is a test.",
        speaker="A",
        start="00:00:00",
        end="00:00:10",
        timestamp_start=0,
        timestamp_end=10,
    )


@pytest.fixture
def dummy_empty_transcript() -> BaseTranscript:
    """Fixture for a dummy BaseTranscript object."""
    utterances = [
        TranscriptUtterance("This is a test", "A", "00:00:00", "00:00:10", 10, 0)
        for _ in range(10)
    ]
    return BaseTranscript(
        transcript_id="transcript_456789",
        transcript=utterances,
    )


@pytest.fixture
def dummy_full_transcript() -> BaseTranscript:
    """Fixture for a dummy BaseTranscript object."""
    utterances = [
        TranscriptUtterance("This is a test", "A", "00:00:00", "00:00:10", 10, 0)
        for _ in range(10)
    ]
    return BaseTranscript(
        transcript_id="transcript_456789",
        transcript=utterances,
        job_id_set=["job_123456"],
        summary_id_set=["summary_123456"],
        speaker_map={"A": "The Speaker", "B": "The Other Speaker"},
    )


@pytest.fixture
def dummy_list_transcripts() -> ListTranscripts:
    """Fixture for a dummy ListTranscripts object."""
    return ListTranscripts(page_count=3, next_page="https://next_page.com", results=[])


def test_transcript_utterance(dummy_transcript_utterance: TranscriptUtterance) -> None:
    """Test the TranscriptUtterance object."""
    assert dummy_transcript_utterance.text == "This is a test."
    assert dummy_transcript_utterance.speaker == "A"
    assert dummy_transcript_utterance.timestamp_start == 0
    assert dummy_transcript_utterance.timestamp_end == 10
    assert dummy_transcript_utterance.start == "00:00:00"
    assert dummy_transcript_utterance.end == "00:00:10"
    assert isinstance(dummy_transcript_utterance, TranscriptUtterance)


@pytest.mark.parametrize(
    "utterance",
    [
        [1, "A", "00:00:00", "00:00:10", 0, 10],
        ["This is a test", 1, "00:00:00", "00:00:10", 0, 10],
        ["This is a test", "A", "00:00:00", "00:00:10", 10, 0],
    ],
)
def test_wrong_transcript_utterance(utterance: List[Union[str, int]]) -> None:
    """Test the TranscriptUtterance object."""
    with pytest.raises((TypeError, ValueError)):
        TranscriptUtterance(
            text=utterance[0],  # type: ignore
            speaker=utterance[1],  # type: ignore
            start_index=utterance[2],
            end_index=utterance[3],
        )


def test_transcript(dummy_empty_transcript: BaseTranscript) -> None:
    """Test the BaseTranscript object."""
    assert dummy_empty_transcript.transcript_id == "transcript_456789"
    assert dummy_empty_transcript.transcript == [
        TranscriptUtterance("This is a test", "A", "00:00:00", "00:00:10", 10, 0)
        for _ in range(10)
    ]
    assert isinstance(dummy_empty_transcript, BaseTranscript)
    assert dummy_empty_transcript.job_id_set == list()
    assert dummy_empty_transcript.summary_id_set == list()
    assert dummy_empty_transcript.speaker_map == {}

    assert dummy_empty_transcript.transcript[0].text == "This is a test"
    assert dummy_empty_transcript.transcript[0].speaker == "A"
    assert dummy_empty_transcript.transcript[0].start == "00:00:00"
    assert dummy_empty_transcript.transcript[0].end == "00:00:10"
    assert dummy_empty_transcript.transcript[0].timestamp_start == 0
    assert dummy_empty_transcript.transcript[0].timestamp_end == 10

    assert hasattr(dummy_empty_transcript, "add_job_id") and callable(
        dummy_empty_transcript.add_job_id
    )
    assert hasattr(dummy_empty_transcript, "add_summary_id") and callable(
        dummy_empty_transcript.add_summary_id
    )
    assert hasattr(dummy_empty_transcript, "update_speaker_map") and callable(
        dummy_empty_transcript.update_speaker_map
    )

    dummy_empty_transcript.add_job_id("job_123456")
    assert dummy_empty_transcript.job_id_set == ["job_123456"]
    assert isinstance(dummy_empty_transcript.job_id_set, list)

    dummy_empty_transcript.add_summary_id("summary_123456")
    assert dummy_empty_transcript.summary_id_set == ["summary_123456"]
    assert isinstance(dummy_empty_transcript.summary_id_set, list)

    dummy_empty_transcript.update_speaker_map(
        {"A": "The Speaker", "B": "The Other Speaker"}
    )
    assert dummy_empty_transcript.speaker_map == {
        "A": "The Speaker",
        "B": "The Other Speaker",
    }
    assert isinstance(dummy_empty_transcript.speaker_map, dict)


def test_full_transcript(dummy_full_transcript: BaseTranscript) -> None:
    """Test the BaseTranscript object."""
    assert dummy_full_transcript.transcript_id == "transcript_456789"
    assert dummy_full_transcript.transcript == [
        TranscriptUtterance("This is a test", "A", "00:00:00", "00:00:10", 10, 0)
        for _ in range(10)
    ]
    assert isinstance(dummy_full_transcript, BaseTranscript)
    assert dummy_full_transcript.job_id_set == ["job_123456"]
    assert dummy_full_transcript.summary_id_set == ["summary_123456"]
    assert dummy_full_transcript.speaker_map == {
        "A": "The Speaker",
        "B": "The Other Speaker",
    }

    assert dummy_full_transcript.transcript[0].text == "This is a test"
    assert dummy_full_transcript.transcript[0].speaker == "A"
    assert dummy_full_transcript.transcript[0].start == "00:00:00"
    assert dummy_full_transcript.transcript[0].end == "00:00:10"
    assert dummy_full_transcript.transcript[0].timestamp_start == 0
    assert dummy_full_transcript.transcript[0].timestamp_end == 10

    assert hasattr(dummy_full_transcript, "add_job_id") and callable(
        dummy_full_transcript.add_job_id
    )
    assert hasattr(dummy_full_transcript, "add_summary_id") and callable(
        dummy_full_transcript.add_summary_id
    )
    assert hasattr(dummy_full_transcript, "update_speaker_map") and callable(
        dummy_full_transcript.update_speaker_map
    )

    dummy_full_transcript.add_job_id("job_123456")
    assert dummy_full_transcript.job_id_set == ["job_123456"]
    dummy_full_transcript.add_job_id("job_987654")
    assert dummy_full_transcript.job_id_set == ["job_123456", "job_987654"]

    dummy_full_transcript.add_summary_id("summary_123456")
    assert dummy_full_transcript.summary_id_set == ["summary_123456"]
    dummy_full_transcript.add_summary_id("summary_987654")
    assert dummy_full_transcript.summary_id_set == ["summary_123456", "summary_987654"]

    dummy_full_transcript.update_speaker_map({})
    assert dummy_full_transcript.speaker_map == {}
    dummy_full_transcript.update_speaker_map(
        {"A": "The Speaker", "B": "The Other Speaker"}
    )
    assert dummy_full_transcript.speaker_map == {
        "A": "The Speaker",
        "B": "The Other Speaker",
    }


@pytest.mark.parametrize(
    "speaker_map",
    [
        {1: "The Speaker", 2: "The Other Speaker"},
        {"A": 1, "B": 2},
        {"A": "The Speaker", "B": 2},
        {"A": 1, "B": "The Other Speaker"},
    ],
)
def test_speaker_map_creation(
    speaker_map: Dict[Union[str, int], Union[str, int]]
) -> None:
    """Test the BaseTranscript object speaker_map creation."""
    with pytest.raises(TypeError):
        BaseTranscript("transcript_456789", speaker_map=speaker_map)  # type: ignore


def test_list_transcripts(dummy_list_transcripts: ListTranscripts) -> None:
    """Test the ListTranscripts object."""
    assert dummy_list_transcripts is not None
    assert dummy_list_transcripts.page_count == 3
    assert dummy_list_transcripts.next_page == "https://next_page.com"
    assert dummy_list_transcripts.results == []
