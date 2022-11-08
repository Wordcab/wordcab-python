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

"""Wordcab API Config variables."""

AVAILABLE_AUDIO_FORMATS = [".flac", ".m4a", ".mp3", ".mpga", ".ogg", ".wav"]
AVAILABLE_GENERIC_FORMATS = [".json", ".txt"]
AVAILABLE_PLAN = ["free", "paid"]
EXTRACT_AVAILABLE_STATUS = [
    "Deleted", "Error", "Extracting", "ExtractionComplete", "ItemQueued", "Pending", "PreparingExtraction",
]
SUMMARY_TYPES = ["conversational", "narrative", "no_speaker", "reason_conclusion"]
SUMMARIZE_AVAILABLE_STATUS = [
    "Deleted",
    "Error",
    "ItemQueued",
    "Pending",
    "PreparingSummary",
    "PreparingTranscript",
    "Summarizing",
    "SummaryComplete",
    "Transcribing",
    "TranscriptComplete",
]
