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

"""Test suite for the source dataclasses."""

import pytest
from pathlib import Path

from wordcab.core_objects import (
    BaseSource,
    GenericSource,
    LocalSource,
    RemoteSource,
)
from wordcab.core_objects.source import AVAILABLE_AUDIO_FORMATS


@pytest.fixture
def dummy_base_source() -> BaseSource:
    """Fixture for a dummy BaseSource object."""
    return BaseSource(source_type="generic")


@pytest.fixture
def dummy_local_source() -> LocalSource:
    """Fixture for a dummy LocalSource object."""
    return LocalSource(source_type="generic", filepath=Path(__file__))


@pytest.fixture
def dummy_remote_source() -> RemoteSource:
    """Fixture for a dummy RemoteSource object."""
    return RemoteSource(source_type="generic", url="https://example.com")


@pytest.fixture
def dummy_generic_source_with_filepath() -> GenericSource:
    """Fixture for a dummy GenericSource object."""
    return GenericSource(source_type="generic", filepath=Path(__file__))


@pytest.fixture
def dummy_generic_source_with_url() -> GenericSource:
    """Fixture for a dummy GenericSource object."""
    return GenericSource(source_type="generic", url="https://example.com")


def test_available_audio_formats() -> None:
    """Test the AVAILABLE_AUDIO_FORMATS object."""
    assert AVAILABLE_AUDIO_FORMATS == [".flac", ".m4a", ".mp3", ".mpga", ".ogg", ".wav"]


def test_base_source(dummy_base_source: BaseSource) -> None:
    """Test the BaseSource object."""
    assert dummy_base_source.source_type == "generic"


def test_local_source(dummy_local_source: LocalSource) -> None:
    """Test the LocalSource object."""
    assert dummy_local_source.source_type == "generic"
    assert dummy_local_source.filepath == Path(__file__)


def test_remote_source(dummy_remote_source: RemoteSource) -> None:
    """Test the RemoteSource object."""
    assert dummy_remote_source.source_type == "generic"
    assert dummy_remote_source.url == "https://example.com"


def test_generic_source_with_filepath(
    dummy_generic_source_with_filepath: GenericSource,
) -> None:
    """Test the GenericSource object."""
    assert dummy_generic_source_with_filepath.source_type == "generic"
    assert dummy_generic_source_with_filepath.filepath == Path(__file__)
    assert dummy_generic_source_with_filepath.url is None


def test_generic_source_with_url(
    dummy_generic_source_with_url: GenericSource,
) -> None:
    """Test the GenericSource object."""
    assert dummy_generic_source_with_url.source_type == "generic"
    assert dummy_generic_source_with_url.filepath is None
    assert dummy_generic_source_with_url.url == "https://example.com"
