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
)
from wordcab.core_objects.source import AVAILABLE_AUDIO_FORMATS


@pytest.fixture
def dummy_generic_source_with_filepath() -> GenericSource:
    """Fixture for a dummy GenericSource object."""
    return GenericSource(filepath=Path(__file__))


@pytest.fixture
def dummy_generic_source_with_url() -> GenericSource:
    """Fixture for a dummy GenericSource object."""
    return GenericSource(url="https://example.com")


def test_available_audio_formats() -> None:
    """Test the AVAILABLE_AUDIO_FORMATS object."""
    assert AVAILABLE_AUDIO_FORMATS == [".flac", ".m4a", ".mp3", ".mpga", ".ogg", ".wav"]


def test_base_source() -> None:
    """Test the BaseSource object."""
    with pytest.raises(ValueError):
        BaseSource()
        BaseSource(filepath=Path(__file__), url="https://example.com")
        BaseSource(url="123456")
    with pytest.raises(TypeError):
        BaseSource(filepath=123456)
    with pytest.raises(FileNotFoundError):
        BaseSource(filepath=Path("/tmp/does_not_exist"))

    base = BaseSource(filepath=Path(__file__))
    assert base.filepath == Path(__file__)
    assert base.url is None
    assert base.source_type == "local"
    assert base._stem == Path(__file__).stem
    assert base._suffix == Path(__file__).suffix

    base = BaseSource(url="https://example.com")
    assert base.filepath is None
    assert base.url == "https://example.com"
    assert base.source_type == "remote"

    assert hasattr(base, "_load_file_from_path")
    assert callable(getattr(base, "_load_file_from_path"))
    assert hasattr(base, "_load_file_from_url")
    assert callable(getattr(base, "_load_file_from_url"))


def test_generic_source_with_filepath(
    dummy_generic_source_with_filepath: GenericSource,
) -> None:
    """Test the GenericSource object."""
    assert dummy_generic_source_with_filepath.filepath == Path(__file__)
    assert dummy_generic_source_with_filepath.url is None
    assert dummy_generic_source_with_filepath.source_type == "local"
    assert dummy_generic_source_with_filepath._stem == Path(__file__).stem
    assert dummy_generic_source_with_filepath._suffix == Path(__file__).suffix


def test_generic_source_with_url(
    dummy_generic_source_with_url: GenericSource,
) -> None:
    """Test the GenericSource object."""
    assert dummy_generic_source_with_url.filepath is None
    assert dummy_generic_source_with_url.url == "https://example.com"
    assert dummy_generic_source_with_url.source_type == "remote"
