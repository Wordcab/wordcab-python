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

"""Wordcab API Login."""

import logging
import os
from getpass import getpass
from pathlib import Path
from typing import Optional

import requests  # type: ignore

from .config import WORDCAB_TOKEN_FOLDER


logger = logging.getLogger(__name__)

path_to_token = Path(WORDCAB_TOKEN_FOLDER).expanduser()


def login(account: str, token: Optional[str] = None) -> None:
    """Login to Wordcab API."""
    if token is not None:
        _login(account, token)
    else:
        raise ValueError(
            "Please provide a token or use `wordcab login` command to login from CLI."
        )


def cli_login() -> None:
    """
    Login to Wordcab API from CLI.

    This function is called from the CLI, prompting the user for their
    credentials and then storing them as git credentials.
    """
    logger.warning(
        r"""
         _  _   __   ____  ____   ___   __   ____
        / )( \ /  \ (  _ \(    \ / __) / _\ (  _ \
        \ /\ /(  O ) )   / ) D (( (__ /    \ ) _ (
        (_/\_) \__/ (__\_)(____/ \___)\_/\_/(____/

        To login, please use your API token generated from https://wordcab.com/account/api-key/
        """
    )
    account = input("    Email: ")
    token = getpass("    API Token: ")
    _login(account, token)


def cli_logout() -> None:
    """
    Logout from Wordcab API from CLI.

    This function is called from the CLI, prompting the user for their email
    address and then removing their stored git credentials.
    """
    logger.warning(
        r"""
     _  _   __   ____  ____   ___   __   ____
    / )( \ /  \ (  _ \(    \ / __) / _\ (  _ \
    \ /\ /(  O ) )   / ) D (( (__ /    \ ) _ (
    (_/\_) \__/ (__\_)(____/ \___)\_/\_/(____/

    To logout, please enter your email address.
        """
    )
    account = input("    Email: ")
    _logout(account)


def get_token() -> Optional[str]:
    """Read API token from git credential store."""
    token = os.environ.get("WORDCAB_API_KEY")
    if token is None:
        try:
            return path_to_token.read_text().split(":")[1]
        except FileNotFoundError:
            pass
    return token


def _check_valid_credentials(account: str, token: str) -> bool:
    """Check if the credentials are valid."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://wordcab.com/api/v1/me", headers=headers)
    if r.status_code == 200:
        if r.json()["account_email"] == account:
            return True
    return False


def _login(account: str, token: str) -> None:
    """Login to Wordcab API."""
    if _check_valid_credentials(account, token):
        path_to_token.parent.mkdir(exist_ok=True)
        with path_to_token.open("w+") as f:
            f.write(f"{account}:{token}")
        logger.warning(
            f"Successfully logged in as {account} . Credentials are stored in {path_to_token}"
        )
    else:
        logger.warning(
            f"Invalid credentials for {account} . Please check your API token."
        )


def _logout(account: str) -> None:
    """Logout from Wordcab API."""
    path_to_token.unlink()
    logger.warning(
        f"Successfully logged out as {account} . Credentials are removed from {path_to_token}"
    )
