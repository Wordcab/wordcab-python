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

```{eval-rst}
.. autoclass:: wordcab.Client
   :members:
```
