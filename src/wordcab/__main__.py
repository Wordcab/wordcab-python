"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Wordcab Python SDK."""


if __name__ == "__main__":
    main(prog_name="wordcab-python")  # pragma: no cover
