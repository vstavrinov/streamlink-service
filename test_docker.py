import os
from urllib.request import urlopen
import query_cases
from time import sleep

if 'endpoint' in os.environ:
    endpoint = os.environ['endpoint']
else:
    endpoint = 'http://localhost:8000?'


class TestQuery(query_cases.TestCases):

    def probe(self, args, count):
        sleep(2)
        return urlopen(endpoint + args).read(count)
