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

"""Wordcab API Job object."""

import logging
from dataclasses import dataclass, field

from .source import Source


logger = logging.getLogger(__name__)


@dataclass
class JobSettings:
    """Wordcab API Job Settings object."""

    ephemeral_data: bool = field(init=False, default=False)
    pipeline: str = field(init=False, default=None)
    only_api: bool = field(init=False, default=True)
    split_long_utterances: bool = field(init=False, default=False)


@dataclass
class Job:
    """Wordcab API Job object."""

    display_name: str
    job_name: str
    job_status: str = field(init=False, default="Pending")
    settings: JobSettings = field(init=False, default_factory=dict)
    source: Source = field(init=False, default=None)
    time_started: str = field(init=False, default=None)
    transcript_id: str = field(init=False, default=None)
