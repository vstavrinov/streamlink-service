import os
import unittest

if 'test_url' in os.environ:
    url = os.environ['test_url']
else:
    url = 'ok.ru/videoembed/73364'
sample = '474000'


class TestCases(unittest.TestCase):

    def probe(self, args, count):
        '''Make actual query to the service. Redefined in child class'''
        pass

    def test_video(self):
        '''Get video stream by implicit parameter'''
        args = url
        args += '+best'
        self.assertTrue(self.probe(args, len(sample)//2).hex() == sample)

    def test_url(self):
        '''Get video stream by explicit parameter'''
        args = 'url=' + url
        args += '+best'
        self.assertTrue(self.probe(args, len(sample)//2).hex() == sample)

    def test_proxy(self):
        '''Query for stream via proxy'''
        if 'test_proxy' in os.environ:
            args = url
            args += '+best'
            args += '&https-proxy=' + os.environ['test_proxy']
            args += '&http-timeout=60'
            self.assertTrue(self.probe(args, len(sample)//2).hex() == sample)
        else:
            self.assertTrue(True)

    def test_path(self):
        '''Drop last char from url to get exception.'''
        args = url[:-1]
        self.assertTrue('Available streams: []' in self.probe(args, None).decode())

    def test_host(self):
        '''Drop first char from url to get exception.'''
        args = url[1:]
        self.assertTrue(' NoPluginError: ' in self.probe(args, None).decode())

    def test_streams(self):
        '''Check for available streams (worst ... best)'''
        args = url
        self.assertTrue('Available streams: ' in self.probe(args, None).decode())

    def test_help(self):
        '''Pull out long help message'''
        args = 'help'
        self.assertTrue('**Available options**:' in self.probe(args, None).decode())
