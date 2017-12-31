# PhraseFinder Python Client

[PhraseFinder](http://phrasefinder.io) is a search engine for the [Google Books Ngram Dataset](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html) (version 2). This repository contains the official Python client for requesting PhraseFinder's web [API](http://phrasefinder.io/api) which is free to use for any purpose.

* [Documentation](http://phrasefinder.io/documentation)
* [Python API Reference](https://mtrenkmann.github.io/phrasefinder-client-python/)

## Demo

```python
from __future__ import print_function
import phrasefinder as pf

def main():
    """Requests the PhraseFinder web service and prints out the result."""

    # Set up your query.
    query = 'I like ???'

    # Optional: set the maximum number of phrases to return.
    options = pf.SearchOptions()
    options.topk = 10

    # Send the request.
    try:
        result = pf.search(pf.Corpus.AmericanEnglish, query, options)
        if result.status != pf.Status.Ok:
            print('Request was not successful: {}'.format(result.status))
            return

        # Print phrases line by line.
        for phrase in result.phrases:
            print("{0:6f}".format(phrase.score), end="")
            for token in phrase.tokens:
                print(" {}".format(token.text), end="")
            print()

    except Exception as error:
        print('Some error occurred: {}'.format(error))


if __name__ == '__main__':
    main()
```

## How to run the demo

```sh
git clone https://github.com/mtrenkmann/phrasefinder-client-python.git
cd phrasefinder-client-python
python src/demo.py
```

## Output

```plain
0.175468 I like to think of
0.165350 I like to think that
0.149246 I like it . "
0.104326 I like it , "
0.091746 I like the way you
0.082627 I like the idea of
0.064459 I like that . "
0.057900 I like it very much
0.055201 I like you . "
0.053677 I like the sound of
```

## Installation

Copy the file `src/phrasefinder.py` into the source directory of your project.
