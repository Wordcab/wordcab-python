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

from ..config import EXTRACT_AVAILABLE_STATUS, SUMMARIZE_AVAILABLE_STATUS
from .source import BaseSource


logger = logging.getLogger(__name__)


@dataclass
class JobSettings:
    """Wordcab API Job Settings object."""

    ephemeral_data: bool = field(init=False, default=False)
    pipeline: str = field(init=False, default=None)
    only_api: bool = field(init=False, default=True)
    split_long_utterances: bool = field(init=False, default=False)


@dataclass
class BaseJob:
    """Wordcab API BaseJob object."""

    display_name: str
    job_name: str
    settings: JobSettings
    source: BaseSource
    time_started: str
    transcript_id: str
    job_status: str = "Pending"

    def __post_init__(self) -> None:
        """Post-init method."""
        logger.info(f"Job {self.job_name} created.")

    def job_update(self, **kwargs) -> None:
        """Update the job attributes."""
        for key, value in kwargs.items():
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

    def __post_init__(self) -> None:
        """Post-init."""
        super().__post_init__()
        self._job_type = "SummarizeJob"
        self.available_status = SUMMARIZE_AVAILABLE_STATUS
