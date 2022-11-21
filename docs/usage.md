# Usage

## Installation

```bash
$ pip install wordcab
```

## Login

In order to use the API, you need to login first.

```bash
$ wordcab login

>>>         _  _   __   ____  ____   ___   __   ____
>>>        / )( \ /  \ (  _ \(    \ / __) / _\ (  _ \
>>>        \ /\ /(  O ) )   / ) D (( (__ /    \ ) _ (
>>>        (_/\_) \__/ (__\_)(____/ \___)\_/\_/(____/
>>>
>>>        To login, please use your API token generated from https://wordcab.com/account/api-key/
>>>
>>>    Email:
>>>    API Token: 
```

Enter your email and API token. You can get your API token from [https://wordcab.com/account/api-key/](https://wordcab.com/account/api-key/).

Once you are logged in, you can use the API with any python script.

## Simple functions

You can use the API with simple functions like `get_stats` by importing it from `wordcab`.

```python
>>> from wordcab import get_stats

>>> stats = get_stats()
>>> stats
{
  "account_email": "thomas@wordcab.com",
  "plan": "free",
  "monthly_request_limit": "1000",
  "request_count": 152,
  "minutes_summarized": 10,
  "transcripts_summarized": 147,
  "metered_charge": "$26.76",
  "min_created": "2022-10-17T17:42:06Z",
  "max_created": "2022-11-17T17:42:06Z"
}
```

## Client

You can also use the API with a client object.

```python
>>> from wordcab import Client

>>> with Client() as client:
...     stats = client.get_stats()
...     print(stats)
...
{
  "account_email": "thomas@wordcab.com",
  "plan": "free",
  "monthly_request_limit": "1000",
  "request_count": 152,
  "minutes_summarized": 10,
  "transcripts_summarized": 147,
  "metered_charge": "$26.76",
  "min_created": "2022-10-17T17:42:06Z",
  "max_created": "2022-11-17T17:42:06Z"
}
```

## Available functions

Check out the [Reference](reference.md) for a list of available functions.

name | client | simple
--- | --- | ---
get_stats | ✅ | ✅
start_summary | ✅ | ✅
start_extract | ✅ | ✅
list_jobs | ✅ | ✅
list_summaries | ✅ | ✅
list_transcripts | ✅ | ✅
retrieve_job | ✅ | ✅
retrieve_summary | ✅ | ✅
retrieve_transcript | ✅ | ✅
delete_job | ✅ | ✅
change_speaker_labels | ✅ | ✅
