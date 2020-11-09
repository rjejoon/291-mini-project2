import unittest

from phase1.main import termFilter

class TestTermFilter(unittest.TestCase):

    def test_termFilter(self):
        self.assertAlmostEqual(termFilter('''";:?.,!Hello<p></p>'''), 'Hello')
        
