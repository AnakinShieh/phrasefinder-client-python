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

try:
    # Python 2.
    import urllib as urllibx
except ImportError:
    # Python 3.
    import urllib.request as urllibx

class Corpus(object):
    EnglishUS, EnglishGB, Spanish, French, German, Russian, Chinese = range(7)
    _to_string = {
        EnglishUS: "eng-us",
        EnglishGB: "eng-gb",
        Spanish:   "spa",
        French:    "fre",
        German:    "ger",
        Russian:   "rus",
        Chinese:   "chi"
    }

class Status(object):
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
    class Tag(object):
        Given, Inserted, Alternative, Completed = range(4)
    def __init__(self):
        self.text = ""
        self.tag  = Token.Tag.Given

class Phrase(object):
    def __init__(self):
        self.tokens       = []  # List of Phrase.Token instances.
        self.match_count  = 0
        self.volume_count = 0
        self.first_year   = 0
        self.last_year    = 0
        self.relative_id  = 0
        self.score        = 0.0

class Options(object):
    def __init__(self):
        self.corpus = Corpus.EnglishUS
        self.nmin   = 1
        self.nmax   = 5
        self.topk   = 100
        self.key    = ""

class Result(object):
    def __init__(self):
        self.status  = Status.Ok
        self.phrases = []  # List of Phrase instances.
        self.quota   = 0

def search(query, options = Options()):
    file = urllibx.urlopen(_to_url(query, options))
    result = Result()
    result.status = Status._from_http_response_code[file.getcode()]
    if result.status == Status.Ok:
        result.quota = int(file.info()["X-Quota"])
        for line in file.readlines():
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
    return "http://phrasefinder.io/search?" + urllibx.urlencode(params)

