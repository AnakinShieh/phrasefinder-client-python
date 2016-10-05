# This file is part of PhraseFinder.  http://phrasefinder.io
#
# Copyright (C) 2016  Martin Trenkmann
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module phrasefinder provides routines for querying the PhraseFinder web service
at http://phrasefinder.io.
"""
import sys
if sys.version_info[0] < 3:  # this check is correct
    # Python 2.
    import urllib as urllibx
    from urllib import urlencode as urlencode
else:
    # Python 3.
    import urllib.request as urllibx
    from urllib.parse import urlencode as urlencode

version = 1000 # major * 10^6 + minor * 10^3 + micro
"""Defines the version number as one integer."""

class Corpus(object):
    """
    Corpus contains numeric constants that represent corpora to be searched.
    All corpora belong to version 2 of the Google Books Ngram Dataset
    (http://storage.googleapis.com/books/ngrams/books/datasetsv2.html).
    """
    EnglishUS, EnglishGB, Spanish, French, German, Russian, Chinese = range(7)
    _to_string = {
        EnglishUS: "eng-us",
        EnglishGB: "eng-gb",
        Spanish:   "spa",
        French:    "fre",
        German:    "ger",
        Russian:   "rus",
        Chinese:   "chi"  # Simplyfied Chinese
    }

class Status(object):
    """
    Status contains numeric constants that report whether a request was
    successful or not. The value is derived from the HTTP status code sent along
    with a response. Note that the numeric value does not correspond to the
    original HTTP code.
    """
    Ok, BadRequest, PaymentRequired, MethodNotAllowed, TooManyRequests, ServerError = range(6)
    _from_http_response_code = {
        200: Ok,
        400: BadRequest,
        402: PaymentRequired,
        405: MethodNotAllowed,
        429: TooManyRequests,
        500: ServerError
    }

class Token(object):
    """
    Token represents a single token (word, punctuation mark, etc.) as part of a
    phrase.
    """
    class Tag(object):
        """
        Tag denotes the role of a token with respect to the query.
        """
        Given, Inserted, Alternative, Completed = range(4)
    def __init__(self):
        self.text = ""
        self.tag  = Token.Tag.Given

class Phrase(object):
    """
    Phrase represents a phrase, also called n-gram.
    A phrase consists of a sequence of tokens and metadata.
    """
    def __init__(self):
        self.tokens       = []   # The tokens of the phrase.
        self.match_count  = 0    # The absolute frequency in the corpus.
        self.volume_count = 0    # The number of books it appears in.
        self.first_year   = 0    # Publication date of the first book it appears in.
        self.last_year    = 0    # Publication date of the last book it appears in.
        self.relative_id  = 0    # See the API documentation on the website.
        self.score        = 0.0  # The relative frequency it matched the given query.

class Options(object):
    """
    Options represents optional parameters that can be sent along with a query.
    """
    def __init__(self):
        self.corpus = Corpus.EnglishUS
        self.nmin   = 1
        self.nmax   = 5
        self.topk   = 100
        self.key    = ""

class Result(object):
    """
    Result represents a search result.
    """
    def __init__(self):
        self.status  = Status.Ok
        self.phrases = []  # List of Phrase instances.
        self.quota   = 0

def search(query, options = Options()):
    """
    Search sends a request to the server.
    The second argument can be nil to go with default parameters.
    It returns a Result object whose status field is equal to StatusOk if the
    request was successful. In this case other fields of the object are in valid
    state and can be read. Any status other than StatusOk indicates a failed
    request. In that case other fields in the result have unspecified data.
    Critical errors are reported via err that is not nil.
    """
    file = urllibx.urlopen(_to_url(query, options))
    result = Result()
    result.status = Status._from_http_response_code[file.getcode()]
    if result.status == Status.Ok:
        result.quota = int(file.info()["X-Quota"])
        for line in file.readlines():
            line = line.decode('utf-8')  # needed because py3 reads bytes via urllib
            phrase = Phrase()
            parts = line.split("\t")
            for token_with_tag in parts[0].split(" "):
                token = Token()
                token.text = token_with_tag[:-2]
                token.tag  = int(token_with_tag[-1])
                phrase.tokens.append(token)
            phrase.match_count  = int(parts[1])
            phrase.volume_count = int(parts[2])
            phrase.first_year   = int(parts[3])
            phrase.last_year    = int(parts[4])
            phrase.relative_id  = int(parts[5])
            phrase.score        = float(parts[6])
            result.phrases.append(phrase)
    file.close()
    return result

def _to_url(query, options):
    params = [
        ("format", "tsv"),
        ("query", query),
        ("corpus", Corpus._to_string[options.corpus]),
        ("nmin", options.nmin),
        ("nmax", options.nmax),
        ("topk", options.topk)
    ]
    if options.key:
        params.append(("key", options.key))
    return "http://phrasefinder.io/search?" + urlencode(params)

