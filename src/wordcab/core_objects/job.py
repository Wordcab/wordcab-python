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

"""Wordcab API Job object."""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from ..config import (
    EXTRACT_AVAILABLE_STATUS,
    SOURCE_OBJECT_MAPPING,
    SUMMARIZE_AVAILABLE_STATUS,
)


logger = logging.getLogger(__name__)


@dataclass
class JobSettings:
    """Wordcab API Job Settings object."""

    ephemeral_data: Optional[bool] = field(default=False)
    pipeline: str = field(default="default")
    only_api: Optional[bool] = field(default=True)
    split_long_utterances: Optional[bool] = field(default=False)

    def __post_init__(self) -> None:
        """Post init."""
        if self.pipeline == "default":
            raise ValueError("Pipeline must be set to a valid pipeline name")


@dataclass
class BaseJob:
    """Wordcab API BaseJob object."""

    display_name: str
    job_name: str
    source: str
    job_status: Optional[str] = field(default="Pending")
    metadata: Optional[Dict[str, str]] = field(default=None)
    settings: Optional[JobSettings] = field(default=None)
    tags: Optional[List[str]] = field(default=None)
    time_started: Optional[str] = field(default=None)
    time_completed: Optional[str] = field(default=None)
    transcript_id: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """Post-init method."""
        logger.info(f"Job {self.job_name} created.")
        if self.source not in SOURCE_OBJECT_MAPPING.keys():
            raise ValueError(
                f"""
                Source {self.source} is not a valid source. Valid sources are {SOURCE_OBJECT_MAPPING.keys()}.
            """
            )

    def job_update(self, parameters: Dict[str, str]) -> None:
        """Update the job attributes."""
        for key, value in parameters.items():
            if key in self.__dict__:
                if getattr(self, key) != value:
                    setattr(self, key, value)
                    logger.info(f"Job {self.job_name} updated: {key} = {value}")
                else:
                    logger.info(f"Job {self.job_name} not updated: {key} = {value}")
            else:
                logger.warning(
                    f"Cannot update {key} in {self.job_name}, not a valid attribute."
                )


@dataclass
class ExtractJob(BaseJob):
    """Wordcab API ExtractJob object."""

    def __post_init__(self) -> None:
        """Post-init."""
        super().__post_init__()
        self._job_type = "ExtractJob"
        self.available_status = EXTRACT_AVAILABLE_STATUS


@dataclass
class SummarizeJob(BaseJob):
    """Wordcab API SummarizeJob object."""

    summary_details: Optional[Dict[str, str]] = field(default=None)

    def __post_init__(self) -> None:
        """Post-init."""
        super().__post_init__()
        self._job_type = "SummarizeJob"
        self.available_status = SUMMARIZE_AVAILABLE_STATUS


@dataclass
class ListJobs:
    """Wordcab API ListJobs object."""

    page_count: int
    next_page: str
    results: List[Union[ExtractJob, SummarizeJob]]
