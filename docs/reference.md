# Reference

## Simple functions

Simple functions are available for all API endpoints. You can use them by importing them from `wordcab`.

```python
>>> from wordcab import get_stats

>>> stats = get_stats()
>>> stats
Stats(...)
```

They are simple wrappers around the client object. You can use the client object directly if you need more control.

### get_stats

```{eval-rst}
.. autofunction:: wordcab.get_stats
```

### start_summary

```{eval-rst}
.. autofunction:: wordcab.start_summary
```

### start_extract

```{eval-rst}
.. autofunction:: wordcab.start_extract
```

### list_jobs

```{eval-rst}
.. autofunction:: wordcab.list_jobs
```

### list_summaries

```{eval-rst}
.. autofunction:: wordcab.list_summaries
```

### list_transcripts

```{eval-rst}
.. autofunction:: wordcab.list_transcripts
```

### retrieve_job

```{eval-rst}
.. autofunction:: wordcab.retrieve_job
```

### retrieve_summary

```{eval-rst}
.. autofunction:: wordcab.retrieve_summary
```

### retrieve_transcript

```{eval-rst}
.. autofunction:: wordcab.retrieve_transcript
```

### delete_job

```{eval-rst}
.. autofunction:: wordcab.delete_job
```

### change_speaker_labels

```{eval-rst}
.. autofunction:: wordcab.change_speaker_labels
```

## Client

The client object is the main interface to the API. You can use it to access all API endpoints.

```python
from wordcab import Client

client = Client()
stats = client.get_stats()

# Run with a context manager
with Client() as client:
   stats = client.get_stats()

# Run with a context manager and a custom API key
with Client(api_key="my_api_key") as client:
   stats = client.get_stats()
```

```{eval-rst}
.. autoclass:: wordcab.Client
   :members:
```

## Core objects

The core objects are used to represent the data returned by the API but also to pass data to the API.

### Source objects

#### BaseSource

The BaseSource object is the base class for all source objects. It is not meant to be used directly.

```{eval-rst}
.. autoclass:: wordcab.core_objects.BaseSource
   :members:
```

#### AudioSource

The AudioSource object is required to create a job that uses an audio file as input.

```python
>>> from wordcab.core_objects import AudioSource

>>> audio_source = AudioSource(filepath="path/to/audio/file.mp3")
>>> audio_source
AudioSource(...)
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.AudioSource
   :members:
```

#### GenericSource

The GenericSource object is required to create a job that uses a generic file as input,
such as `.txt` or `.json`.

```python
>>> from wordcab.core_objects import GenericSource

>>> generic_source = GenericSource(filepath="path/to/generic/file.txt")
>>> generic_source
GenericSource(...)
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.GenericSource
   :members:
```

#### InMemorySource

The InMemorySource object is required to create a job that uses a pre-loaded transcript as input.
It is useful when you want to create a job from a transcript that you have already loaded in memory.

```python
>>> from wordcab.core_objects import InMemorySource

>>> transcript = {
>>>   "transcript": ["SPEAKER A: Hello.", "SPEAKER B: Hi."]
>>> }
>>> in_memory_source = InMemorySource(in_memory_obj=transcript)
>>> in_memory_source
InMemorySource(...)
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.InMemorySource
   :members:
```

### Job objects

```{eval-rst}
.. autoclass:: wordcab.core_objects.BaseJob
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.ExtractJob
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.JobSettings
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.ListJobs
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.SummarizeJob
   :members:
```

### Stats object

```{eval-rst}
.. autoclass:: wordcab.core_objects.Stats
   :members:
```

### Summary objects

```{eval-rst}
.. autoclass:: wordcab.core_objects.BaseSummary
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.ConclusionSummary
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.ListSummaries
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.ReasonSummary
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.StructuredSummary
   :members:
```

### Transcript objects

```{eval-rst}
.. autoclass:: wordcab.core_objects.BaseTranscript
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.ListTranscripts
   :members:
```

```{eval-rst}
.. autoclass:: wordcab.core_objects.TranscriptUtterance
   :members:
```
