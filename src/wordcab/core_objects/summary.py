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

"""Wordcab API Summary object."""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Union


logger = logging.getLogger(__name__)


SUMMARY_TYPES = ["conversational", "narrative", "no_speaker", "reason_conclusion"]


@dataclass
class StructuredSummary:
    """Structured summary object."""

    end: str
    start: str
    summary: str
    summary_html: str
    timestamps_end: int
    timestamps_start: int
    transcript_segment: Dict[str, Union[str, int]] = field(default_factory=dict)

    def __post_init__(self):
        """Post-init."""
        if not isinstance(self.end, str):
            raise TypeError(f"end must be a string, not {type(self.end)}")
        if len(self.end.split(":")) != 3:
            raise ValueError(f"end must be in the format 'HH:MM:SS', not {self.end}")

        if not isinstance(self.start, str):
            raise TypeError(f"start must be a string, not {type(self.start)}")
        if len(self.start.split(":")) != 3:
            raise ValueError(f"start must be in the format 'HH:MM:SS', not {self.start}")

        if not isinstance(self.summary, str):
            raise TypeError(f"summary must be a string, not {type(self.summary)}")
        if not isinstance(self.summary_html, str):
            raise TypeError(f"summary_html must be a string, not {type(self.summary_html)}")

        if not isinstance(self.timestamps_end, int):
            raise TypeError(f"timestamps_end must be an integer, not {type(self.timestamps_end)}")
        if self.timestamps_end != self._convert_timestamp(self.end):
            raise ValueError(f"timestamps_end must be equal to end, not {self.timestamps_end}")

        if not isinstance(self.timestamps_start, int):
            raise TypeError(f"timestamps_start must be an integer, not {type(self.timestamps_start)}")
        if self.timestamps_start != self._convert_timestamp(self.start):
            raise ValueError(f"timestamps_start must be equal to start, not {self.timestamps_start}")
    
    def _convert_timestamp(self, timestamp: str) -> int:
        """Convert a timestamp to milliseconds."""
        hours, minutes, seconds = timestamp.split(":")
        return int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000


@dataclass
class BaseSummary:
    """Summary object."""

    job_status: str
    summary_id: str
    display_name: str = field(default=None)
    job_name: str = field(default=None)
    process_time: str = field(default=None)
    speaker_map: Dict[str, str] = field(default=None)
    source: str = field(default=None)
    summary_type: str = field(default=None)
    summary: Dict[str, Union[Dict[str, str], Dict[str, List[StructuredSummary]]]] = field(default=None)
    transcript_id: str = field(default=None)
    time_started: str = field(default=None)
    time_completed: str = field(default=None)

    def __post_init__(self):
        """Post init."""
        if self.summary_type:
            if self.summary_type not in SUMMARY_TYPES:
                raise ValueError(f"Summary type must be one of {SUMMARY_TYPES}, not {self.summary_type}")

        if self.time_started and self.time_completed:
            if self.time_started == self.time_completed:
                raise ValueError("time_started and time_completed must be different")