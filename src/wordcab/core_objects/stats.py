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

"""Wordcab API Stats object."""

import logging
from dataclasses import dataclass, field
from typing import List, Optional

import validators  # type: ignore

from ..config import AVAILABLE_PLAN


logger = logging.getLogger(__name__)


@dataclass
class Stats:
    """Stats object for the Wordcab API."""

    account_email: str
    plan: str
    monthly_request_limit: str
    request_count: int
    minutes_summarized: int
    transcripts_summarized: int
    metered_charge: str
    min_created: str
    max_created: str
    tags: Optional[List[str]] = field(default=None)

    def __post_init__(self) -> None:
        """Post-init method."""
        if self.plan not in AVAILABLE_PLAN:
            raise ValueError(f"Plan must be one of {AVAILABLE_PLAN}, not {self.plan}")

        if not validators.email(self.account_email):
            raise ValueError(
                f"Please provide a valid email address, not {self.account_email}"
            )

        # Check if metered charge is in the right format $X or $X.XX
        if not self.metered_charge.startswith("$"):
            raise ValueError(
                f"Metered charge must start with $, not {self.metered_charge}"
            )
        if not self.metered_charge[1:].replace(".", "", 1).isdigit():
            raise ValueError(
                f"Metered charge must be a number, not {self.metered_charge}"
            )

        if self.min_created > self.max_created:
            raise ValueError(
                f"min_created must be before max_created, not {self.min_created} and {self.max_created}"
            )
