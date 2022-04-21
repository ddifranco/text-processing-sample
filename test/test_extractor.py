#! /usr/bin/python3

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
from extractor import Extractor

class TestExtractor(unittest.TestCase):

    e = Extractor()

    def test_ex1(self):

        istring = "VISUAL ACUITY:      CC    OD: 20/40+1  OS: 20/20"
        expected = (40,  20, None, None)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex2(self):

        istring = "VISUAL ACUITY:      corrected    OD   20/30-1  OS   20/40+1"
        expected = (30, 40, None, None)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex3(self):

        istring = "VACC OD: 20/30   OS: 20/20"
        expected = (30, 20, None, None)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex4(self):

        istring = "VA:     CC     OD    20/200       OS   20/"
        expected = (200, None, None, None)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex5(self):

        istring = "VISUAL ACUITY:      CC    RE: 20/       LE: 20/"
        expected = (None, None, None, None)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex6(self):

        istring = "VISUAL ACUITY   CC       OD: 20/40   OS: 20/30       PH  OD: 20/20   OS: 20/20"
        expected = (40, 30, 20, 20)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex7(self):

        istring = "VA:   CC:   RE 20/40    LE 20/50       PH: RE 20/30   LE 20/40"
        expected = (40, 50, 30, 40)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex8(self):

        istring = "va   corrected   od 20/200   os  20/30   pinhole  od  20/100   os  20/"
        expected = (200, 30, 100,  None)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex9(self):

        istring = "VISUAL ACUITY:   CC    OD: 20/50    OS: 20/30       PH  OD: 20/40   OS: 20/20"
        expected = (50, 30, 40, 20)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex10(self):

        istring = "VISUAL ACUITY:  corrected      OD 20/20 OS 20/30       PH  OD: 20/   OS: 20/"
        expected = (20,  30,  None,  None)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex11(self):

        istring = "VACC   RE: 20/40-2 LE: 20/20      PH  RE: NI"
        expected = (40,  20,  888,  None)
        self.assertEqual(expected, self.e.extract(istring))

    def test_ex12(self):
        
        istring = "VA   CC   RE 20/400     LE 20/200      PH  RE  20/100   LE NI"
        expected = (400,  200,  100,  888)
        self.assertEqual(expected, self.e.extract(istring))

if __name__ == "__main__":

    unittest.main()
