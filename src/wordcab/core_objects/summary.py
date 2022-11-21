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

"""Wordcab API Summary object."""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from ..config import SUMMARY_TYPES


logger = logging.getLogger(__name__)


@dataclass
class StructuredSummary:
    """Structured summary object."""

    end: str
    start: str
    summary: str
    summary_html: str
    timestamp_end: int
    timestamp_start: int
    transcript_segment: Optional[List[Dict[str, Union[str, int]]]] = field(default=None)

    def __post_init__(self) -> None:  # noqa: C901
        """Post-init."""
        if not isinstance(self.end, str):
            raise TypeError(f"end must be a string, not {type(self.end)}")
        if len(self.end.split(":")) != 3:
            raise ValueError(f"end must be in the format 'HH:MM:SS', not {self.end}")

        if not isinstance(self.start, str):
            raise TypeError(f"start must be a string, not {type(self.start)}")
        if len(self.start.split(":")) != 3:
            raise ValueError(
                f"start must be in the format 'HH:MM:SS', not {self.start}"
            )

        if not isinstance(self.summary, str):
            raise TypeError(f"summary must be a string, not {type(self.summary)}")
        if not isinstance(self.summary_html, str):
            raise TypeError(
                f"summary_html must be a string, not {type(self.summary_html)}"
            )

        if not isinstance(self.timestamp_end, int):
            raise TypeError(
                f"timestamp_end must be an integer, not {type(self.timestamp_end)}"
            )

        if not isinstance(self.timestamp_start, int):
            raise TypeError(
                f"timestamp_start must be an integer, not {type(self.timestamp_start)}"
            )


@dataclass
class BaseSummary:
    """Summary object."""

    job_status: str
    summary_id: str
    display_name: Optional[str] = field(default=None)
    job_name: Optional[str] = field(default=None)
    process_time: Optional[str] = field(default=None)
    speaker_map: Optional[Dict[str, str]] = field(default=None)
    source: Optional[str] = field(default=None)
    summary_type: Optional[str] = field(default=None)
    summary: Optional[Dict[str, Dict[str, List[StructuredSummary]]]] = field(
        default=None
    )
    transcript_id: Optional[str] = field(default=None)
    time_started: Optional[str] = field(default=None)
    time_completed: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """Post init."""
        if self.summary_type:
            if self.summary_type not in SUMMARY_TYPES:
                raise ValueError(
                    f"Summary type must be one of {SUMMARY_TYPES}, not {self.summary_type}"
                )

        if self.time_started and self.time_completed:
            if self.time_started == self.time_completed:
                raise ValueError("time_started and time_completed must be different")


@dataclass
class ListSummaries:
    """List summaries object."""

    page_count: int
    next_page: str
    results: List[BaseSummary]
