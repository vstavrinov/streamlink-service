from urllib.request import urlopen
import unittest
import query_cases

endpoint = 'http://localhost:8000/?'


class TestQuery(query_cases.TestCases):

    def probe(self, args, count):
        return urlopen(endpoint + args).read(count)


if __name__ == '__main__':
    unittest.main()
