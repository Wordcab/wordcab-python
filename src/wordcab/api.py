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

"""Wordcab API mapping functions."""

from typing import Dict, Optional

from .client import Client


def request(method: str, api_key: Optional[str] = None, **kwargs) -> Dict:
    """Make a request to the Wordcab API."""
    with Client(api_key=api_key) as client:
        return client.request(method=method, **kwargs)


def get_stats(api_key: Optional[str] = None) -> Dict:
    """Retrieve account stats such as spend and request volume, by timestamp or tag."""
    return request(method="get_stats", api_key=api_key)


def start_extract(api_key: Optional[str] = None, **kwargs) -> Dict:
    """Start an extraction job."""
    return request(method="start_extract", api_key=api_key, **kwargs)


def start_summary(api_key: Optional[str] = None, **kwargs) -> Dict:
    """Start a summary job."""
    return request(method="start_summary", api_key=api_key, **kwargs)


def list_jobs(api_key: Optional[str] = None) -> Dict:
    """Retrieve a list of jobs."""
    return request(method="list_jobs", api_key=api_key)


def retrieve_job(api_key: Optional[str] = None, **kwargs) -> Dict:
    """Retrieve a job."""
    return request(method="retrieve_job", api_key=api_key, **kwargs)


def delete_job(api_key: Optional[str] = None, **kwargs) -> Dict:
    """Delete a job."""
    return request(method="delete_job", api_key=api_key, **kwargs)


def list_transcripts(api_key: Optional[str] = None) -> Dict:
    """Retrieve a list of transcripts."""
    return request(method="list_transcripts", api_key=api_key)


def retrieve_transcript(api_key: Optional[str] = None, **kwargs) -> Dict:
    """Retrieve a transcript."""
    return request(method="retrieve_transcript", api_key=api_key, **kwargs)


def change_speaker_labels(api_key: Optional[str] = None, **kwargs) -> Dict:
    """Change speaker labels."""
    return request(method="change_speaker_labels", api_key=api_key, **kwargs)


def list_summaries(api_key: Optional[str] = None) -> Dict:
    """Retrieve a list of summaries."""
    return request(method="list_summaries", api_key=api_key)


def retrieve_summary(api_key: Optional[str] = None, **kwargs) -> Dict:
    """Retrieve a summary."""
    return request(method="retrieve_summary", api_key=api_key, **kwargs)
