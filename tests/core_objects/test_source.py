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

from pathlib import Path

import pytest

from wordcab.config import AVAILABLE_AUDIO_FORMATS
from wordcab.core_objects import (
    AssemblyAISource,
    AudioSource,
    BaseSource,
    DeepgramSource,
    GenericSource,
    RevSource,
    SignedURLSource,
    VTTSource,
    WordcabTranscriptSource,
)


def test_available_audio_formats() -> None:
    """Test the AVAILABLE_AUDIO_FORMATS object."""
    assert AVAILABLE_AUDIO_FORMATS == [".flac", ".m4a", ".mp3", ".mpga", ".ogg", ".wav"]


def test_base_source(tmp_path: Path) -> None:
    """Test the BaseSource object."""
    path = f"{tmp_path}/test.txt"
    with open(path, "w") as f:
        f.write("test")

    with pytest.raises(ValueError):
        BaseSource()
    with pytest.raises(ValueError):
        BaseSource(filepath=Path(path), url="https://example.com")
    with pytest.raises(ValueError):
        BaseSource(url="123456")
    with pytest.raises(TypeError):
        BaseSource(filepath=123456)
    with pytest.raises(FileNotFoundError):
        BaseSource(filepath=Path(f"{tmp_path}/does_not_exist.txt"))

    base = BaseSource(filepath=Path(path))
    assert base.filepath == Path(path)
    assert base.url is None
    assert base.source_type == "local"
    assert base._stem == Path(path).stem
    assert base._suffix == Path(path).suffix

    base = BaseSource(url="https://example.com")
    assert base.filepath is None
    assert base.url == "https://example.com"
    assert base.source_type == "remote"

    assert hasattr(base, "_load_file_from_path") and callable(base._load_file_from_path)
    assert hasattr(base, "_load_file_from_url") and callable(base._load_file_from_url)

    base = BaseSource(filepath=path)
    assert base.filepath == Path(path)
    assert isinstance(base.filepath, Path)


def test_generic_source_with_filepath(tmp_path: Path) -> None:
    """Test the GenericSource object."""
    path = f"{tmp_path}/test.txt"
    with open(path, "w") as f:
        f.write("test")

    generic_source = GenericSource(filepath=Path(path))
    assert generic_source.filepath == Path(path)
    assert generic_source.url is None
    assert generic_source.source_type == "local"
    assert generic_source._stem == Path(path).stem
    assert generic_source._suffix == Path(path).suffix
    assert generic_source.file_object is not None

    md_path = f"{tmp_path}/test.md"
    with open(md_path, "w") as f:
        f.write("test")

    with pytest.raises(ValueError):
        GenericSource(filepath=Path(md_path))


def test_generic_source_with_url() -> None:
    """Test the GenericSource object."""
    with pytest.raises(NotImplementedError):
        GenericSource(url="https://example.com")


def test_audio_source(tmp_path: Path) -> None:
    """Test the AudioSource object."""
    path = f"{tmp_path}/test.mp3"
    with open(path, "w") as f:
        f.write("test")

    audio_source = AudioSource(filepath=Path(path))
    assert audio_source.filepath == Path(path)
    assert audio_source.url is None
    assert audio_source.source_type == "local"
    assert audio_source._stem == Path(path).stem
    assert audio_source._suffix == Path(path).suffix
    assert audio_source.file_object is not None

    aac_path = f"{tmp_path}/test.aac"
    with open(aac_path, "w") as f:
        f.write("test")

    with pytest.raises(ValueError):
        AudioSource(filepath=Path(aac_path))
    with pytest.raises(NotImplementedError):
        AudioSource(url="https://example.com")


def test_signed_url_source() -> None:
    """Test the SignedURLSource object."""
    with pytest.raises(NotImplementedError):
        SignedURLSource(url="https://example.com")


def test_wordcab_transcript_source() -> None:
    """Test the WordcabTranscriptSource object."""
    with pytest.raises(NotImplementedError):
        WordcabTranscriptSource(url="https://example.com")


def test_rev_source() -> None:
    """Test the RevSource object."""
    with pytest.raises(NotImplementedError):
        RevSource(url="https://example.com")


def test_vtt_source() -> None:
    """Test the VTTSource object."""
    with pytest.raises(NotImplementedError):
        VTTSource(url="https://example.com")


def test_assembly_ai_source() -> None:
    """Test the AssemblyAISource object."""
    with pytest.raises(NotImplementedError):
        AssemblyAISource(url="https://example.com")


def test_deepgram_source() -> None:
    """Test the DeepgramSource object."""
    with pytest.raises(NotImplementedError):
        DeepgramSource(url="https://example.com")
