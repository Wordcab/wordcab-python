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

from typing import List, Optional

from .client import Client
from .core_objects import BaseSource, Stats, SummarizeJob


def request(method: str, api_key: Optional[str] = None, **kwargs) -> None:
    """Make a request to the Wordcab API."""
    with Client(api_key=api_key) as client:
        return client.request(method=method, **kwargs)


def get_stats(
    min_created: Optional[str] = None,
    max_created: Optional[str] = None,
    tags: Optional[List[str]] = None,
    api_key: Optional[str] = None,
) -> Stats:
    """
    Retrieve account stats such as spend and request volume, by timestamp or tag.

    Parameters
    ----------
    min_created : str, optional
        The minimum limit of the specified time range. The default is None. If
        None, the minimum limit will be automatically set to a month prior.
    max_created : str
        The maximum limit of the specified time range. The default is None. If
        None, the maximum limit will be automatically set to the current time.
    tags : list of str, optional
        A list of tags to filter by. The default is None. If None, no tags will
        be used to filter the stats.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    Stats
        The stats object containing the stats data.
    """
    return request(
        method="get_stats",
        min_created=min_created,
        max_created=max_created,
        tags=tags,
        api_key=api_key,
    )


def start_extract(api_key: Optional[str] = None, **kwargs) -> None:
    """Start an extraction job."""
    return request(method="start_extract", api_key=api_key, **kwargs)


def start_summary(source_object: BaseSource, display_name: str, api_key: Optional[str] = None) -> SummarizeJob:
    """
    Start a summary job.

    Parameters
    ----------
    source_object : BaseSource
        The source object to summarize.
    display_name : str
        The display name of the summary. This is useful for retrieving the
        job later.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.
    
    Returns
    -------
    SummarizeJob
        The summarize job object.
    """
    return request(method="start_summary", source_object=source_object, display_name=display_name, api_key=api_key)


def list_jobs(api_key: Optional[str] = None) -> None:
    """Retrieve a list of jobs."""
    return request(method="list_jobs", api_key=api_key)


def retrieve_job(api_key: Optional[str] = None, **kwargs) -> None:
    """Retrieve a job."""
    return request(method="retrieve_job", api_key=api_key, **kwargs)


def delete_job(api_key: Optional[str] = None, **kwargs) -> None:
    """Delete a job."""
    return request(method="delete_job", api_key=api_key, **kwargs)


def list_transcripts(api_key: Optional[str] = None) -> None:
    """Retrieve a list of transcripts."""
    return request(method="list_transcripts", api_key=api_key)


def retrieve_transcript(api_key: Optional[str] = None, **kwargs) -> None:
    """Retrieve a transcript."""
    return request(method="retrieve_transcript", api_key=api_key, **kwargs)


def change_speaker_labels(api_key: Optional[str] = None, **kwargs) -> None:
    """Change speaker labels."""
    return request(method="change_speaker_labels", api_key=api_key, **kwargs)


def list_summaries(api_key: Optional[str] = None) -> None:
    """Retrieve a list of summaries."""
    return request(method="list_summaries", api_key=api_key)


def retrieve_summary(api_key: Optional[str] = None, **kwargs) -> None:
    """Retrieve a summary."""
    return request(method="retrieve_summary", api_key=api_key, **kwargs)
