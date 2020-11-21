import unittest
import json
import os

from phase1.extractTermsFrom import extractTermsFrom

class TestExtractTermsFrom(unittest.TestCase):

    def test_ExtractTermsFrom(self):
        f_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'test.json')
        with open(f_path, 'r') as f:
            docList = json.load(f)['row']

        test_doc1 = docList[0]
        result = ['abc', 'def', 'ghi', 'jklmn', 'What', 'the', 'and', 'software', 'hardware', 'mac']
        print(extractTermsFrom(test_doc1))
        self.assertListEqual(sorted(extractTermsFrom(test_doc1)), sorted(result))

        # extracting terms from url link
        test_doc2 = docList[1]
        result = ['href', 'http', 'www', 'lobotomo', 'com', 'products', 'IPSecuritas']
        self.assertListEqual(sorted(extractTermsFrom(test_doc2)), sorted(result))

