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

from typing import Dict, List, Optional, Union, no_type_check

from .client import Client
from .core_objects import (
    BaseSource,
    BaseSummary,
    BaseTranscript,
    ExtractJob,
    InMemorySource,
    ListJobs,
    ListSummaries,
    ListTranscripts,
    Stats,
    SummarizeJob,
)


@no_type_check
def request(
    method: str,
    api_key: Optional[str] = None,
    **kwargs: Union[bool, int, str, Dict[str, str], List[int], List[str]]
) -> Union[
    BaseSource,
    BaseSummary,
    BaseTranscript,
    ExtractJob,
    ListJobs,
    ListSummaries,
    ListTranscripts,
    Stats,
    SummarizeJob,
    Union[ExtractJob, SummarizeJob],
]:
    """Make a request to the Wordcab API."""
    with Client(api_key=api_key) as client:
        return client.request(method=method, **kwargs)


@no_type_check
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


@no_type_check
def start_extract(
    source_object: Union[BaseSource, InMemorySource],
    display_name: str,
    ephemeral_data: Optional[bool] = False,
    only_api: Optional[bool] = True,
    pipelines: Union[str, List[str]] = [  # noqa: B006
        "questions_answers",
        "topic_segments",
        "emotions",
        "speaker_talk_ratios",
    ],
    split_long_utterances: bool = False,
    tags: Optional[Union[str, List[str]]] = None,
    api_key: Optional[str] = None,
) -> ExtractJob:
    """
    Start an extraction job.

    Parameters
    ----------
    source_object : BaseSource or InMemorySource
        The source object to use for the extraction job.
    display_name : str
        The display name of the extraction job. This is useful for retrieving the job later.
    ephemeral_data : bool, optional
        Whether to delete the data after the job is complete. The default is False. If False, the data will be
        kept on WordCab's servers. You can delete the data at any time, check the documentation here:
        https://docs.wordcab.com/docs/enabling-ephemeral-data
    only_api : bool, optional
        Whether to only use the API for the extraction job. The default is True.
    pipelines : list of str, optional
        A list of pipelines to use for the extraction job. The default is ["questions_answers", "topic_segments",
        "emotions", "speaker_talk_ratios"]. You can use one or more of the available pipelines.
    split_long_utterances : bool
        Whether to split long utterances into multiple shorter utterances. The default is False.
    tags : str or list of str, optional
        The tags to add to the job. The default is None. If None, no tags will be added.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    ExtractJob
        The extract job object.
    """
    return request(
        method="start_extract",
        source_object=source_object,
        display_name=display_name,
        ephemeral_data=ephemeral_data,
        only_api=only_api,
        pipelines=pipelines,
        split_long_utterances=split_long_utterances,
        tags=tags,
        api_key=api_key,
    )


@no_type_check
def start_summary(
    source_object: Union[BaseSource, InMemorySource],
    display_name: str,
    summary_type: str,
    ephemeral_data: bool = False,
    only_api: bool = True,
    pipelines: Union[str, List[str]] = ["transcribe", "summarize"],  # noqa: B006
    source_lang: Optional[str] = None,
    split_long_utterances: bool = False,
    summary_length: Union[int, List[int]] = 3,
    tags: Optional[Union[str, List[str]]] = None,
    api_key: Optional[str] = None,
) -> SummarizeJob:
    """
    Start a summary job.

    Parameters
    ----------
    source_object : BaseSource or InMemorySource
        The source object to summarize.
    display_name : str
        The display name of the summary. This is useful for retrieving the job later.
    summary_type : str
        The type of summary to create. You can choose from "conversational", "narrative", "reason_conclusion" or
        "no_speaker". More information can be found here: https://docs.wordcab.com/docs/summary-types
    ephemeral_data : bool
        Whether to delete the data after the summary is created. The default is False. If False, the data will be
        kept on Wordcab's servers. You can delete the data at any time, check the documentation here:
        https://docs.wordcab.com/docs/enabling-ephemeral-data
    only_api : bool
        Whether to only use the API to create the summary. The default is True.
    pipelines : str or list of str
        The pipelines to use. The default is ["transcribe", "summarize"].
    source_lang : str, optional
        The language of the source. If None, the language will be `en` (English) by default.
    split_long_utterances : bool
        Whether to split long utterances into multiple shorter utterances. The default is False.
    summary_length : int or list of int, optional
        The length of the summary. The default is 3. The length should be between 1 and 5. If a list of ints is
        provided, the summary will be created for each length.
    tags : str or list of str, optional
        The tags to add to the job. The default is None. If None, no tags will be added.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    SummarizeJob
        The summarize job object.
    """
    return request(
        method="start_summary",
        source_object=source_object,
        display_name=display_name,
        summary_type=summary_type,
        ephemeral_data=ephemeral_data,
        only_api=only_api,
        pipelines=pipelines,
        source_lang=source_lang,
        split_long_utterances=split_long_utterances,
        summary_length=summary_length,
        tags=tags,
        api_key=api_key,
    )


@no_type_check
def list_jobs(
    page_size: int = 100, order_by: str = "-time_started", api_key: Optional[str] = None
) -> ListJobs:
    """
    Retrieve a list of jobs.

    Parameters
    ----------
    page_size : int
        The number of jobs to retrieve per page. The default is 100.
    order_by : str
        The order to retrieve the jobs in. The default is "-time_started".
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    ListJobs
        The list jobs object containing the list of jobs. The jobs can be
        SummarizeJob or ExtractJob objects.
    """
    return request(
        method="list_jobs", page_size=page_size, order_by=order_by, api_key=api_key
    )


@no_type_check
def retrieve_job(
    job_name: str, api_key: Optional[str] = None
) -> Union[ExtractJob, SummarizeJob]:
    """
    Retrieve a job by name.

    Parameters
    ----------
    job_name : str
        The name of the job to retrieve.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    ExtractJob or SummarizeJob
        The job object. The job can be an ExtractJob or SummarizeJob object.
    """
    return request(method="retrieve_job", job_name=job_name, api_key=api_key)


@no_type_check
def delete_job(job_name: str, api_key: Optional[str] = None) -> Dict[str, str]:
    """
    Delete a job by name and all associated data (including the transcript).

    Note that this will delete the transcript from WordCab's servers. If you want to keep the transcript,
    you should download it before deleting the job.

    Parameters
    ----------
    job_name: str
        The name of the job to delete.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    Dict[str, str]
        A dictionary containing the name of the deleted job.
    """
    return request(method="delete_job", job_name=job_name, api_key=api_key)


@no_type_check
def list_transcripts(
    page_size: int = 100, api_key: Optional[str] = None
) -> ListTranscripts:
    """
    Retrieve a list of transcripts.

    Parameters
    ----------
    page_size : int
        The number of transcripts to retrieve per page. The default is 100.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    ListTranscripts
        The list transcripts object containing the list of transcripts.
    """
    return request(method="list_transcripts", page_size=page_size, api_key=api_key)


@no_type_check
def retrieve_transcript(
    transcript_id: str, api_key: Optional[str] = None
) -> BaseTranscript:
    """
    Retrieve a transcript by id.

    Parameters
    ----------
    transcript_id : str
        The id of the transcript to retrieve.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    BaseTranscript
        The transcript object.
    """
    return request(
        method="retrieve_transcript", transcript_id=transcript_id, api_key=api_key
    )


@no_type_check
def change_speaker_labels(
    transcript_id: str, speaker_map: Dict[str, str], api_key: Optional[str] = None
) -> BaseTranscript:
    """
    Change speaker labels in a transcript.

    Parameters
    ----------
    transcript_id : str
        The id of the transcript to change the speaker labels of.
    speaker_map : Dict[str, str]
        A dictionary mapping the old speaker labels to the new speaker labels.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    BaseTranscript
        The transcript object with the changed speaker labels.
    """
    return request(
        method="change_speaker_labels",
        transcript_id=transcript_id,
        speaker_map=speaker_map,
        api_key=api_key,
    )


@no_type_check
def list_summaries(
    page_size: int = 100, api_key: Optional[str] = None
) -> ListSummaries:
    """
    Retrieve a list of summaries.

    Parameters
    ----------
    page_size : int
        The number of summaries to retrieve per page. The default is 100.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    ListSummaries
        The list summaries object containing the list of summaries.
    """
    return request(method="list_summaries", page_size=page_size, api_key=api_key)


@no_type_check
def retrieve_summary(summary_id: str, api_key: Optional[str] = None) -> BaseSummary:
    """
    Retrieve a summary by id.

    Parameters
    ----------
    summary_id : str
        The id of the summary to retrieve.
    api_key : str, optional
        The API key to use. The default is None. If None, the API key will be
        automatically retrieved from the environment variable WORDCAB_API_KEY.

    Returns
    -------
    BaseSummary
        The summary object.
    """
    return request(method="retrieve_summary", summary_id=summary_id, api_key=api_key)
