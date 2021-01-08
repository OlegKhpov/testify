from django.test import TestCase
from core.frange import frange, Frange


class TestFrange(TestCase):
    def test_frange(self):
        self.assertEqual(list(frange(5)), [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5])

        self.assertEqual(list(Frange(5)), [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5])
        self.assertEqual(list(Frange(2, 10, 2)), [2, 4, 6, 8])
