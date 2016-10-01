# PhraseFinder Python Client

The official Python client for the [PhraseFinder](http://phrasefinder.io) web service

* [Documentation](https://mtrenkmann.github.io/phrasefinder-client-python/)

## Demo

```python
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
            print 'Request was not successful: %d' % result.status
            return

        # Print phrases line by line.
        for phrase in result.phrases:
            print '%6f' % phrase.score,
            for token in phrase.tokens:
                print '%s_%d' % (token.text, token.tag),
            print
        print 'Remaining quota: %d' % result.quota

    except Exception, e:
        print 'Some error occurred: %s' % e


if __name__ == '__main__':
    main()
```

### Run

```sh
python ./src/demo.py
```

### Output

```
0.175468 I_0 like_0 to_1 think_1 of_1
0.165350 I_0 like_0 to_1 think_1 that_1
0.149246 I_0 like_0 it_1 ._1 "_1
0.104326 I_0 like_0 it_1 ,_1 "_1
0.091746 I_0 like_0 the_1 way_1 you_1
0.082627 I_0 like_0 the_1 idea_1 of_1
0.064459 I_0 like_0 that_1 ._1 "_1
0.057900 I_0 like_0 it_1 very_1 much_1
0.055201 I_0 like_0 you_1 ._1 "_1
0.053677 I_0 like_0 the_1 sound_1 of_1
Remaining quota: 99
```

## Installation

Copy the file `src/phrasefinder.py` into the source directory of your project.

