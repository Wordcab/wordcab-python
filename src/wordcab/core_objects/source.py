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

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union, no_type_check

import validators  # type: ignore

from ..config import AVAILABLE_AUDIO_FORMATS, AVAILABLE_GENERIC_FORMATS


logger = logging.getLogger(__name__)


@dataclass
class BaseSource:
    """Base class for all source objects except for InMemorySource. It is not meant to be used directly.

    Parameters
    ----------
    filepath : Optional[Union[str, Path]], optional
        Path to the local file, by default None.
    url : Optional[str], optional
        URL to the remote file, by default None.

    Raises
    ------
    ValueError
        If neither `filepath` nor `url` are provided.
    ValueError
        If both `filepath` and `url` are provided.
    TypeError
        If `filepath` is not a string or a Path object.
    FileNotFoundError
        If `filepath` does not exist or is not accessible.

    Attributes
    ----------
    source : str
        The source type.
    source_type : str
        The source type.
    _stem : str
        The stem of the file.
    _suffix : str
        The suffix of the file.

    Returns
    -------
    BaseSource
        The source object.
    """

    filepath: Optional[Union[str, Path]] = field(default=None, repr=False)
    url: Optional[str] = field(default=None, repr=False)
    source: str = field(init=False)
    source_type: str = field(init=False)
    _stem: str = field(init=False, repr=False)
    _suffix: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Post-init method."""
        self.source = self.__class__.__name__
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

    @no_type_check
    def _load_file_from_path(self) -> bytes:
        """Load file from local path."""
        with open(self.filepath, "rb") as f:
            return f.read()

    def _load_file_from_url(self) -> bytes:
        """Load file from URL."""
        raise NotImplementedError("Loading files from URLs is not implemented yet.")

    def prepare_payload(self) -> Union[str, Dict[str, bytes]]:
        """Prepare payload."""
        raise NotImplementedError("Payload preparation is not implemented yet.")

    def prepare_headers(self) -> Dict[str, str]:
        """Prepare headers."""
        raise NotImplementedError("Headers preparation is not implemented yet.")


@dataclass
class InMemorySource:
    """In-memory source object.

    The in-memory source object is a special case of the generic source object.
    It is used to pass a pre-processed transcript to the API.

    Parameters
    ----------
    obj : Union[Dict[str, List[str]], List[str]]
        The in-memory object. It can be a list of strings or a dict with a `transcript` key
        and a list of strings as value.

    Raises
    ------
    ValueError
        If the in-memory object does not have a `transcript` key.
    TypeError
        If the in-memory object does not have a list as value for the `transcript` key.
    TypeError
        If the in-memory object is not a list or a dict.

    Examples
    --------
    >>> from wordcab.core_objects import InMemorySource

    >>> transcript = {"transcript": ["SPEAKER A: Hello.", "SPEAKER B: Hi."]}
    >>> in_memory_source = InMemorySource(obj=transcript)
    >>> in_memory_source
    InMemorySource(...)
    >>> in_memory_source.obj

    Returns
    -------
    InMemorySource
        The in-memory source object.
    """

    obj: Optional[Union[Dict[str, List[str]], List[str]]] = field(
        default=None, repr=False
    )
    source: str = field(init=False)
    source_type: str = field(init=False)

    def __post_init__(self) -> None:
        """Post-init method."""
        self.source = "generic"
        self.source_type = "in_memory"
        if isinstance(self.obj, dict):
            if "transcript" not in self.obj:
                raise ValueError(
                    "Please provide a valid in-memory object. It must have a `transcript` key."
                )
            elif not isinstance(self.obj["transcript"], list):
                raise TypeError(
                    "Please provide a valid in-memory object. The `transcript` key must be a list."
                )
        elif isinstance(self.obj, list):
            self.obj = {"transcript": self.obj}
        else:
            raise TypeError(
                "Please provide a valid in-memory object. It must be a list or a dict."
            )

    def prepare_payload(self) -> str:
        """Prepare payload for API request."""
        self.payload = json.dumps(self.obj)
        return self.payload

    def prepare_headers(self) -> Dict[str, str]:
        """Prepare headers for API request."""
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        return self.headers


@dataclass
class GenericSource(BaseSource):
    """Generic source object.

    The GenericSource object is required to create a job that uses a generic file as input,
    such as `.txt` or `.json` file.

    Parameters
    ----------
    filepath : Union[str, Path]
        The path to the local file.
    url : str
        The URL to the remote file.

    Raises
    ------
    ValueError
        If the file format is not supported.
    ValueError
        If both `filepath` and `url` are provided.
    TypeError
        If the path is not a string or a Path object.
    FileNotFoundError
        If the file does not exist or is not accessible.

    Examples
    --------
    >>> from wordcab.core_objects import GenericSource

    >>> generic_source = GenericSource(filepath="path/to/generic/file.txt")  # doctest: +SKIP
    >>> generic_source  # doctest: +SKIP
    GenericSource(...)
    >>> generic_source.file_object  # doctest: +SKIP
    b'Hello, world!'
    >>> generic_source.source_type  # doctest: +SKIP
    'local'
    >>> generic_source._suffix  # doctest: +SKIP
    '.txt'
    >>> generic_source._stem  # doctest: +SKIP
    'file'

    Returns
    -------
    GenericSource
        The generic source object.
    """

    file_object: bytes = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        self.source = "generic"
        if self.source_type == "local":
            if self._suffix not in AVAILABLE_GENERIC_FORMATS:
                raise ValueError(
                    f"Please provide a valid file format. {self._suffix} is not valid."
                )
            else:
                self.file_object = self._load_file_from_path()

        if self.source_type == "remote":
            self.file_object = self._load_file_from_url()

    def prepare_payload(self) -> str:
        """Prepare payload for API request."""
        if self._suffix == ".json":
            self.payload = json.dumps({"transcript": json.loads(self.file_object)})
        elif self._suffix == ".txt":
            self.payload = json.dumps(
                {"transcript": self.file_object.decode("utf-8").splitlines()}
            )
        return self.payload

    def prepare_headers(self) -> Dict[str, str]:
        """Prepare headers for API request."""
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        return self.headers


@dataclass
class AudioSource(BaseSource):
    """
    The AudioSource object is required to create a job that uses an audio file as input.

    Parameters
    ----------
    filepath : Union[str, Path]
        The path to the local file.
    url : str
        The URL to the remote file.

    Raises
    ------
    ValueError
        If the file format is not supported.
    ValueError
        If both `filepath` and `url` are provided.
    TypeError
        If the path is not a string or a Path object.
    FileNotFoundError
        If the file does not exist or is not accessible.

    Examples
    --------
    >>> from wordcab.core_objects import AudioSource

    >>> audio_source = AudioSource(filepath="path/to/audio/file.mp3")  # doctest: +SKIP
    >>> audio_source  # doctest: +SKIP
    AudioSource(...)

    Returns
    -------
    AudioSource
        The audio source object.
    """

    file_object: bytes = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        self.source = "audio"
        if self.source_type == "local":
            if self._suffix not in AVAILABLE_AUDIO_FORMATS:
                raise ValueError(
                    f"Please provide a valid file format. {self._suffix} is not valid."
                )
            else:
                self.file_object = self._load_file_from_path()

        if self.source_type == "remote":
            self.file_object = self._load_file_from_url()

    def prepare_payload(self) -> Dict[str, bytes]:
        """Prepare payload for API request."""
        self.payload = {"audio_file": self.file_object}
        return self.payload

    @no_type_check
    def prepare_headers(self) -> dict:
        """Prepare headers for API request."""
        self.headers = {}
        return self.headers


@dataclass
class WordcabTranscriptSource(BaseSource):
    """Wordcab transcript source object."""

    transcript_id: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        if self.transcript_id is None:
            raise ValueError(
                "Please provide a `transcript_id` to initialize a WordcabTranscriptSource object."
            )
        self.source = "wordcab_transcript"
        raise NotImplementedError("Wordcab transcript source is not implemented yet.")


@dataclass
class SignedURLSource(BaseSource):
    """Signed URL source object."""

    signed_url: Optional[str] = field(init=False)

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        self.signed_url = self.url
        self.source = "signed_url"
        raise NotImplementedError("Signed URL source is not implemented yet.")


@dataclass
class AssemblyAISource(BaseSource):
    """AssemblyAI source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        self.source = "assembly_ai"
        raise NotImplementedError("AssemblyAI source is not implemented yet.")


@dataclass
class DeepgramSource(BaseSource):
    """Deepgram source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        self.source = "deepgram"
        raise NotImplementedError("Deepgram source is not implemented yet.")


@dataclass
class RevSource(BaseSource):
    """Rev.ai source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        self.source = "rev_ai"
        raise NotImplementedError("Rev.ai source is not implemented yet.")


@dataclass
class VTTSource(BaseSource):
    """VTT source object."""

    def __post_init__(self) -> None:
        """Post-init method."""
        super().__post_init__()
        self.source = "vtt"
        raise NotImplementedError("VTT source is not implemented yet.")
