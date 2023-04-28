"""
Sample tests    
"""
from django.test import SimpleTestCase

from app import calc

class CalcTest(SimpleTestCase):
    """ Tset the calc.py"""

    def test_add_number(self):

        res = calc.add(5,6)

        self.assertEqual(res, 11)
    
    def test_subtract_number(self):

        res = calc.subtract(15, 10)

        self.assertAlmostEqual(res, 5)

