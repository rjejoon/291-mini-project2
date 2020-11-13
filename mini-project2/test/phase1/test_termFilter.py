import unittest

from phase1.phase1 import termFilter


class TestTermFilter(unittest.TestCase):

    def test_termFilter(self):
        self.assertAlmostEqual(termFilter('''";:?.,!Hello<p></p>'''), 'Hello')
        self.assertAlmostEqual(termFilter('''";:?.,!Hello<p></p>'''), 'Hello')
        self.assertAlmostEqual(termFilter('''";:?.,!Hello<p></p>'''), 'Hello')
        self.assertAlmostEqual(termFilter('''";:?.,!Hello<p></p>'''), 'Hello')
        self.assertAlmostEqual(termFilter('''";:?.,!Hello<p></p>'''), 'Hello')
        
