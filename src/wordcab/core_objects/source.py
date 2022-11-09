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

"""Wordcab API Source object."""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union

import validators

from ..config import AVAILABLE_AUDIO_FORMATS, AVAILABLE_GENERIC_FORMATS


logger = logging.getLogger(__name__)


@dataclass
class BaseSource:
    """Source object."""

    filepath: Union[str, Path] = field(default=None, repr=False)
    url: str = field(default=None, repr=False)
    source_type: str = field(init=False)
    _stem: str = field(init=False, repr=False)
    _suffix: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Post-init method."""
        if not self.filepath and not self.url:
            raise ValueError(
                "Please provide either a local or a remote source, respectively `filepath` or `url`."
            )
        if self.filepath and self.url:
            raise ValueError(
                "Please provide either a local or a remote source, not both `filepath` and `url`."
            )

        if self.filepath:
            if not isinstance(self.filepath, Path) and not isinstance(
                self.filepath, str
            ):
                raise TypeError(
                    f"The path must be a string or a Path object, not {type(self.filepath)}"
                )

            if isinstance(self.filepath, str):
                self.filepath = Path(self.filepath)

            if not self.filepath.exists():
                raise FileNotFoundError(
                    f"File {self.filepath} does not exist or is not accessible."
                )

            self._stem = self.filepath.stem
            self._suffix = self.filepath.suffix
            self.source_type = "local"

        if self.url:
            if not validators.url(self.url):
                raise ValueError(
                    f"Please provide a valid URL. {self.url} is not valid."
                )
            self.source_type = "remote"

    def _load_file_from_path(self) -> bytes:
        """Load file from local path."""
        with open(self.filepath, "rb") as f:
            return f.read()

    def _load_file_from_url(self) -> bytes:
        """Load file from URL."""
        raise NotImplementedError("Loading files from URLs is not implemented yet.")


@dataclass
class GenericSource(BaseSource):
    """Generic source object."""

    file_object: bytes = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        if self.source_type == "local":
            if self._suffix not in AVAILABLE_GENERIC_FORMATS:
                raise ValueError(
                    f"Please provide a valid file format. {self._suffix} is not valid."
                )
            else:
                self.file_object = self._load_file_from_path()

        if self.source_type == "remote":
            self.file_object = self._load_file_from_url()


@dataclass
class AudioSource(BaseSource):
    """Audio source object."""

    file_object: bytes = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        if self.source_type == "local":
            if self._suffix not in AVAILABLE_AUDIO_FORMATS:
                raise ValueError(
                    f"Please provide a valid file format. {self._suffix} is not valid."
                )
            else:
                self.file_object = self._load_file_from_path()

        if self.source_type == "remote":
            self.file_object = self._load_file_from_url()


@dataclass
class WordcabTranscriptSource(BaseSource):
    """Wordcab transcript source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        raise NotImplementedError("Wordcab transcript source is not implemented yet.")


@dataclass
class SignedURLSource(BaseSource):
    """Signed URL source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        raise NotImplementedError("Signed URL source is not implemented yet.")


@dataclass
class AssemblyAISource(BaseSource):
    """AssemblyAI source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        raise NotImplementedError("AssemblyAI source is not implemented yet.")


@dataclass
class DeepgramSource(BaseSource):
    """Deepgram source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        raise NotImplementedError("Deepgram source is not implemented yet.")


@dataclass
class RevSource(BaseSource):
    """Rev.ai source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        raise NotImplementedError("Rev.ai source is not implemented yet.")


@dataclass
class VTTSource(BaseSource):
    """VTT source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        raise NotImplementedError("VTT source is not implemented yet.")
