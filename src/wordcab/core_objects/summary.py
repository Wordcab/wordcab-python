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
from typing import Any, Dict, List, Optional, Union

from ..config import SUMMARY_TYPES


logger = logging.getLogger(__name__)


@dataclass
class StructuredSummary:
    """Structured summary object."""

    summary: str
    summary_html: Optional[str] = field(default=None)
    end: Optional[str] = field(default=None)
    end_index: Optional[int] = field(default=None)
    start: Optional[str] = field(default=None)
    start_index: Optional[int] = field(default=None)
    timestamp_end: Optional[int] = field(default=None)
    timestamp_start: Optional[int] = field(default=None)
    transcript_segment: Optional[List[Dict[str, Union[str, int]]]] = field(default=None)

    def __repr__(self) -> str:
        """Return a string representation of the object without the None values."""
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items() if v is not None)})"


@dataclass
class ReasonSummary:
    """Reason summary object."""

    summary: str
    stop_index: int


@dataclass
class ConclusionSummary:
    """Conclusion summary object."""

    summary: str
    stop_index: int


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
    summary: Optional[Dict[str, Any]] = field(default=None)
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
