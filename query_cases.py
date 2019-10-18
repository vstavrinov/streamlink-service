import os
import unittest

url = 'youtube.com/user/Bloomberg'
sample = '474000'
if 'test_proxy' in os.environ:
    https_proxy = os.environ['test_proxy']
else:
    https_proxy = 'http://51.38.71.101:8080'


class TestCases(unittest.TestCase):

    def probe(self, args, count):
        pass
        '''Make actual query to the service. Redefined in child class'''

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
        args = url
        args += '+best'
        args += '&https-proxy=' + https_proxy
        self.assertTrue(self.probe(args, len(sample)//2).hex() == sample)

    def test_path(self):
        '''Drop last char from url to get exception.'''
        args = url[:-1]
        self.assertTrue(' PluginError: ' in self.probe(args, None).decode())

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
        self.assertTrue('usage: streamlink [OPTIONS] <URL> [STREAM]' in self.probe(args, None).decode())
