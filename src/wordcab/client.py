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

"""Wordcab API Client."""

import logging
import os
from typing import Dict, List, Optional, Union

import requests

from .config import (
    LIST_JOBS_ORDER_BY,
    SOURCE_OBJECT_MAPPING,
    SUMMARY_LENGTHS_RANGE,
    SUMMARY_PIPELINES,
    SUMMARY_TYPES,
)
from .core_objects import BaseSource, ExtractJob, JobSettings, ListJobs, Stats, SummarizeJob
from .utils import (
    _check_summary_length,
    _check_summary_pipelines,
    _format_lengths,
    _format_pipelines,
    _format_tags,
)


logger = logging.getLogger(__name__)


class Client:
    """Wordcab API Client."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the client."""
        self.api_key = api_key if api_key else os.getenv("WORDCAB_API_KEY")
        if not self.api_key:
            # TODO: Add a better error message with cli login instructions
            raise ValueError(
                "API Key not found. You must set the WORDCAB_API_KEY environment variable."
            )

    def __enter__(self) -> "Client":
        """Enter the client context."""
        return self

    def __exit__(
        self,
        exception_type: Optional[Exception],
        exception_value: Optional[Exception],
        traceback: Optional[Exception],
    ) -> None:
        """Exit the client context."""
        pass

    def request(self, method: str, **kwargs) -> None:
        """Make a request to the Wordcab API."""
        if not method:
            raise ValueError("You must specify a method.")
        return getattr(self, method)(**kwargs)

    def get_stats(
        self,
        min_created: Optional[str] = None,
        max_created: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Stats:
        """Get the stats of the account."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        params: Dict[str, str] = {}
        if min_created:
            params["min_created"] = min_created
        if max_created:
            params["max_created"] = max_created
        if tags:
            params["tags"] = tags

        r = requests.get(
            "https://wordcab.com/api/v1/me", headers=headers, params=params
        )

        if r.status_code == 200:
            return Stats(**r.json())
        else:
            raise ValueError(r.text)

    def start_extract(self) -> None:
        """Start an Extraction job."""
        raise NotImplementedError

    def start_summary(
        self,
        source_object: BaseSource,
        display_name: str,
        summary_type: str,
        ephemeral_data: Optional[bool] = False,
        only_api: Optional[bool] = True,
        pipelines: Optional[List[str]] = ["transcribe", "summarize"],
        split_long_utterances: Optional[bool] = False,
        summary_length: Optional[Union[int, List[int]]] = 3,
        tags: Optional[Union[str, List[str]]] = None,
    ) -> None:
        """Start a Summary job."""
        if summary_type not in SUMMARY_TYPES:
            raise ValueError(
                f"Invalid summary type. Available types are: {', '.join(SUMMARY_TYPES)}"
            )

        if _check_summary_length(summary_length) is False:
            raise ValueError(
                f"""
                You must specify a valid summary length. Summary length must be an integer or a list of integers.
                The integer values must be between {SUMMARY_LENGTHS_RANGE[0]} and {SUMMARY_LENGTHS_RANGE[1]}.
            """
            )
        if summary_type == "reason_conclusion" and summary_length:
            logger.warning(
                """
                You have specified a summary length for a reason_conclusion summary but reason_conclusion summaries
                do not use a summary length. The summary_length parameter will be ignored.
            """
            )

        if _check_summary_pipelines(pipelines) is False:
            raise ValueError(
                f"""
                You must specify a valid list of pipelines. Available pipelines are: {", ".join(SUMMARY_PIPELINES)}
            """
            )

        if isinstance(source_object, BaseSource) is False:
            raise ValueError(
                """
                You must specify a valid source object to summarize.
                See https://docs.wordcab.com/docs/accepted-sources for more information.
            """
            )

        source = source_object.source
        if source not in SOURCE_OBJECT_MAPPING.keys():
            raise ValueError(
                f"Invalid source: {source}. Source must be one of {SOURCE_OBJECT_MAPPING.keys()}"
            )
        if source_object.__class__.__name__ != SOURCE_OBJECT_MAPPING[source]:
            raise ValueError(
                f"""
                Invalid source object: {source_object}. Source object must be of type {SOURCE_OBJECT_MAPPING[source]},
                but is of type {type(source_object)}.
            """
            )

        if hasattr(source_object, "payload"):
            payload = source_object.payload
        else:
            payload = source_object.prepare_payload()

        if hasattr(source_object, "headers"):
            headers = source_object.headers
        else:
            headers = source_object.prepare_headers()
        headers["Authorization"] = f"Bearer {self.api_key}"

        params: Dict[str, str] = {
            "source": source,
            "display_name": display_name,
            "ephemeral_data": ephemeral_data,
            "only_api": only_api,
            "pipeline": _format_pipelines(pipelines),
            "split_long_utterances": split_long_utterances,
            "summary_type": summary_type,
            "summary_lens": _format_lengths(summary_length),
        }
        if tags:
            params["tags"] = _format_tags(tags)

        if source == "wordcab_transcript":
            params["transcript_id"] = source_object.transcript_id
        if source == "signed_url":
            params["signed_url"] = source_object.signed_url

        if source == "audio":
            r = requests.post(
                "https://wordcab.com/api/v1/summarize",
                headers=headers,
                params=params,
                files=payload,
            )
        else:
            r = requests.post(
                "https://wordcab.com/api/v1/summarize",
                headers=headers,
                params=params,
                data=payload,
            )

        if r.status_code == 201:
            logger.info("Summary job started.")
            return SummarizeJob(
                display_name=display_name,
                job_name=r.json()["job_name"],
                source=source,
                settings=JobSettings(
                    ephemeral_data=ephemeral_data,
                    pipeline=pipelines,
                    split_long_utterances=split_long_utterances,
                    only_api=only_api,
                ),
            )
        else:
            raise ValueError(r.text)

    def list_jobs(self, page_size: Optional[int] = 100, order_by: Optional[str] = "-time_started") -> None:
        """List all jobs."""
        if order_by not in LIST_JOBS_ORDER_BY:
            raise ValueError(
                f"""
                Invalid `order_by` parameter. Must be one of {LIST_JOBS_ORDER_BY}. 
                You can use - to indicate descending order.
            """
            )

        headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}
        params = {"page_size": page_size, "order_by": order_by}

        r = requests.get(
            "https://wordcab.com/api/v1/jobs", headers=headers, params=params
        )

        if r.status_code == 200:
            data = r.json()
            list_jobs: List[Union[ExtractJob, SummarizeJob]] = []
            for job in data["results"]:
                if "summary_details" in job:
                    list_jobs.append(
                        SummarizeJob(
                            display_name=job["display_name"],
                            job_name=job["job_name"],
                            job_status=job["job_status"],
                            source=job["source"],
                            summary_details=job["summary_details"],
                            transcript_id=job["transcript_id"],
                            time_started=job["time_started"],
                            time_completed=job["time_completed"],
                        )
                    )
                else:
                    list_jobs.append(
                        ExtractJob(
                            display_name=job["display_name"],
                            job_name=job["job_name"],
                            job_status=job["job_status"],
                            source=job["source"],
                            transcript_id=job["transcript_id"],
                            time_started=job["time_started"],
                            time_completed=job["time_completed"],
                        )
                    )
            return ListJobs(page_count=int(data["page_count"]), next_page=data["next"], results=list_jobs)
        else:
            raise ValueError(r.text)

    def retrieve_job(self) -> None:
        """Retrieve a job."""
        raise NotImplementedError

    def delete_job(self) -> None:
        """Delete a job."""
        raise NotImplementedError

    def list_transcripts(self) -> None:
        """List all transcripts."""
        raise NotImplementedError

    def retrieve_transcript(self) -> None:
        """Retrieve a transcript."""
        raise NotImplementedError

    def change_speaker_labels(self) -> None:
        """Change the speaker labels of a transcript."""
        raise NotImplementedError

    def list_summaries(self) -> None:
        """List all summaries."""
        raise NotImplementedError

    def retrieve_summary(self) -> None:
        """Retrieve a summary."""
        raise NotImplementedError
