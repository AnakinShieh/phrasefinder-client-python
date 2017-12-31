#!/usr/bin/env python

"""This module provides routines for querying the PhraseFinder web service."""

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
