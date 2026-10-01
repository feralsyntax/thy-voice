import json
import urllib.error
import urllib.request

QUOTES_URL = "https://zenquotes.io/api/random"


def get_quotes():
    """Return a random quote."""

    try:
        with urllib.request.urlopen(QUOTES_URL, timeout=5) as response:
            data = json.loads(response.read())

        if not data:
            return None

        quote = data[0]

        return {
            "quote": quote["q"],
            "author": quote["a"],
            "permalink": "https://zenquotes.io/",
        }

    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return None
