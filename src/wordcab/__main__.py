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

"""Command-line interface."""
import click

from .login import cli_login, cli_logout


@click.group()
@click.version_option()
def main() -> None:
    """Wordcab Python SDK."""
    pass


@click.command()
def login() -> None:
    """Prompt the user for API credentials and store them as git credentials."""
    cli_login()


@click.command()
def logout() -> None:
    """Remove stored git credentials."""
    cli_logout()


main.add_command(login)
main.add_command(logout)


if __name__ == "__main__":
    main(prog_name="wordcab")  # pragma: no cover
