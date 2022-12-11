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

"""Wordcab API Core Objects."""

from .job import BaseJob, ExtractJob, JobSettings, ListJobs, SummarizeJob
from .source import (
    AssemblyAISource,
    AudioSource,
    BaseSource,
    DeepgramSource,
    GenericSource,
    InMemorySource,
    RevSource,
    SignedURLSource,
    VTTSource,
    WordcabTranscriptSource,
)
from .stats import Stats
from .summary import (
    BaseSummary,
    ConclusionSummary,
    ListSummaries,
    ReasonSummary,
    StructuredSummary,
)
from .transcript import BaseTranscript, ListTranscripts, TranscriptUtterance


__all__ = [
    "AssemblyAISource",
    "AudioSource",
    "BaseJob",
    "BaseSource",
    "BaseSummary",
    "BaseTranscript",
    "ConclusionSummary",
    "DeepgramSource",
    "ExtractJob",
    "GenericSource",
    "InMemorySource",
    "JobSettings",
    "ListJobs",
    "ListSummaries",
    "ListTranscripts",
    "ReasonSummary",
    "RevSource",
    "SignedURLSource",
    "Stats",
    "StructuredSummary",
    "SummarizeJob",
    "TranscriptUtterance",
    "VTTSource",
    "WordcabTranscriptSource",
]
