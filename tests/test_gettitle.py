import unittest

from gettitle import gettitle


class TestCheckAndReconstructUrl(unittest.TestCase):

    def setUp(self):
        self.http_url = "http://google.com"
        self.https_url = "https://google.com"

    def test_correct_url(self):
        ''' Should return same url if the input url is correct. '''

        self.assertEqual(
            self.http_url,
            gettitle.check_and_reconstruct_url(self.http_url)
        )
        self.assertEqual(
            self.https_url,
            gettitle.check_and_reconstruct_url(self.https_url)
        )

    def test_empty_url(self):
        ''' Should return '' for empty url.  '''

        self.assertEqual(
            '',
            gettitle.check_and_reconstruct_url("")
        )

    def test_url_with_leading_space(self):
        ''' Should remove leading space.  '''

        self.assertEqual(
            self.http_url,
            gettitle.check_and_reconstruct_url(" http://google.com")
        )
        self.assertEqual(
            self.https_url,
            gettitle.check_and_reconstruct_url(" https://google.com")
        )

    def test_url_with_leading_spaces(self):
        ''' Should remove leading spaces.  '''

        self.assertEqual(
            self.http_url,
            gettitle.check_and_reconstruct_url("    http://google.com")
        )
        self.assertEqual(
            self.https_url,
            gettitle.check_and_reconstruct_url("    https://google.com")
        )

    def test_url_with_trailing_space(self):
        ''' Should remove trailing space.  '''

        self.assertEqual(
            self.http_url,
            gettitle.check_and_reconstruct_url("http://google.com ")
        )
        self.assertEqual(
            self.https_url,
            gettitle.check_and_reconstruct_url("https://google.com ")
        )

    def test_url_with_trailing_spaces(self):
        ''' Should remove trailing spaces.  '''

        self.assertEqual(
            self.http_url,
            gettitle.check_and_reconstruct_url("http://google.com   ")
        )
        self.assertEqual(
            self.https_url,
            gettitle.check_and_reconstruct_url("https://google.com   ")
        )

    def test_broken_scheme_url(self):
        ''' Should replace scheme which is not http or https to http '''

        self.assertEqual(
            self.http_url,
            gettitle.check_and_reconstruct_url("ttp://google.com")
        )
