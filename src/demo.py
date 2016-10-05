#!/usr/bin/env python
from __future__ import print_function
import phrasefinder


def main():

    # Set up your query.
    query = 'I like ???'

    # Set the optional parameter topk to 10.
    options = phrasefinder.Options()
    options.topk = 10

    # Perform a request.
    try:
        result = phrasefinder.search(query, options)
        if result.status != phrasefinder.Status.Ok:
            print('Request was not successful: {}'.format(result.status))
            return

        # Print phrases line by line.
        for phrase in result.phrases:
            print("{0:6f}".format(phrase.score), end="")
            for token in phrase.tokens:
                print(' {}_{}'.format(token.text, token.tag), end="")
            print()
        print('Remaining quota: {}'.format(result.quota))

    except Exception as error:
        print('Some error occurred: {}'.format(error))


if __name__ == '__main__':
    main()
