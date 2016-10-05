#!/usr/bin/env python

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
