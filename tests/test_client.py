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

import pytest

from wordcab import Client


@pytest.fixture
def client() -> Client:
    """Fixture for a Wordcab Client object."""
    return Client(api_key="dummy_api_key")


def test_client_succeeds(client: Client) -> None:
    """Test client."""
    assert client.api_key == "dummy_api_key"


def test_client_no_api_key() -> None:
    """Test client without an API key."""
    with pytest.raises(ValueError):
        Client(api_key=None)


def test_client_enter_exit(client: Client) -> None:
    """Test client enter and exit methods."""
    with Client(api_key="dummy_api_key") as client:
        assert client.api_key == "dummy_api_key"


def test_request(client: Client) -> None:
    """Test client request method."""
    with pytest.raises(ValueError):
        client.request(method=None)


def test_get_stats(client: Client) -> None:
    """Test client get_stats method."""
    with pytest.raises(NotImplementedError):
        client.get_stats()


def test_start_extract(client: Client) -> None:
    """Test client start_extract method."""
    with pytest.raises(NotImplementedError):
        client.start_extract()


def test_start_summary(client: Client) -> None:
    """Test client start_summary method."""
    with pytest.raises(NotImplementedError):
        client.start_summary()


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
