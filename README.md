# Wordcab Python

[![PyPI](https://img.shields.io/pypi/v/wordcab-python.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/wordcab-python.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/wordcab-python)][python version]
[![License](https://img.shields.io/pypi/l/wordcab-python)][license]

[![Read the documentation at https://wordcab-python.readthedocs.io/](https://img.shields.io/readthedocs/wordcab-python/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/Wordcab/wordcab-python/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/Wordcab/wordcab-python/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/wordcab-python/
[status]: https://pypi.org/project/wordcab-python/
[python version]: https://pypi.org/project/wordcab-python
[read the docs]: https://wordcab-python.readthedocs.io/
[tests]: https://github.com/Wordcab/wordcab-python/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/Wordcab/wordcab-python
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Wordcab

### What is Wordcab?

**Summarize any business communications at scale with Wordcab's API.**

**Wordcab** is a summarization service that provides a simple API to summarize any `audio`, `text`, or `JSON` file.

It also includes compatibility with famous transcripts platforms like [AssemblyAI](https://www.assemblyai.com/),
[Deepgram](https://deepgram.com/), [Rev.ai](https://www.rev.ai/), [Otter.ai](https://otter.ai/), or
[Sonix.ai](https://sonix.ai/).

### Getting started

You can learn more about Wordcab services and pricing on [our website](https://wordcab.com/).

If you want to try out the API, you can [signup](https://wordcab.com/signup/) for a free account and start using the API
right away.

## Requirements

- Os: Linux, Mac, Windows
- Python 3.8+

## Installation

You can install _Wordcab Python_ via [pip] from [PyPI]:

```console
$ pip install wordcab
```

Start using the API with any python script right away:

```python
from wordcab import get_stats

stats = get_stats()
print(stats)
```

## Usage

Please see the [Documentation](https://wordcab-python.readthedocs.io/) for details.

## Contributing

Contributions are very welcome. 🚀
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache 2.0 license][license],
_Wordcab Python SDK_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/Wordcab/wordcab-python/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/Wordcab/wordcab-python/blob/main/LICENSE
[contributor guide]: https://github.com/Wordcab/wordcab-python/blob/main/CONTRIBUTING.md
[command-line reference]: https://wordcab-python.readthedocs.io/en/latest/usage.html
