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

import os
import requests
from typing import Dict, List, Optional

from .core_objects import Stats


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
        tags: Optional[List[str]] = None
    ) -> Stats:
        """Get the stats of the account."""
        headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}
        params: Dict[str, str] = {}
        if min_created:
            params["min_created"] = min_created
        if max_created:
            params["max_created"] = max_created
        if tags:
            params["tags"] = tags

        r = requests.get("https://wordcab.com/api/v1/me", headers=headers, params=params)
        
        if r.status_code == 200:
            return Stats(**r.json())
        else:
            raise ValueError(r.text)

    def start_extract(self) -> None:
        """Start an Extraction job."""
        raise NotImplementedError

    def start_summary(self) -> None:
        """Start a Summary job."""
        raise NotImplementedError

    def list_jobs(self) -> None:
        """List all jobs."""
        raise NotImplementedError

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
