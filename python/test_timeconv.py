import unittest
from timeconv import secs2hhmm,hhmm2secs

class testtimeconv(unittest.TestCase):
    def test_secs2hhmmOK(self):
        self.assertEqual("00:00", secs2hhmm(0))
        self.assertEqual("00:02", secs2hhmm(120))
        self.assertEqual("02:05", secs2hhmm(2*3600 + 5*60))
        self.assertEqual("02:05", secs2hhmm(2*3600 + 5*60 + 55))
        self.assertEqual("12:55", secs2hhmm(12*3600 + 55*60))
        self.assertEqual("12:55", secs2hhmm(12*3600 + 55*60 + 45))
        self.assertEqual("24:00", secs2hhmm(24*3600))
    def test_secs2hhmmKO(self):
        self.assertEqual("00:00", secs2hhmm(-1))
        self.assertEqual("00:00", secs2hhmm(-100))
        self.assertEqual("00:00", secs2hhmm(None))
    def test_hhmm2secsOK(self):
        self.assertEqual(0, hhmm2secs("00:00"))
        self.assertEqual(60, hhmm2secs("00:01"))
        self.assertEqual(3600, hhmm2secs("01:00"))
        self.assertEqual(3600*4 + 30*60, hhmm2secs("04:30"))
    def test_hhmm2secsKO(self):
        self.assertEqual(0, hhmm2secs(""))
        self.assertEqual(0, hhmm2secs("ciao"))
        self.assertEqual(0, hhmm2secs("c"))
        self.assertEqual(0, hhmm2secs(None))

if __name__ == '__main__':
    unittest.main()

