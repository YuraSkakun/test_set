from django.test import SimpleTestCase
from tests import utils


class TestFrange(SimpleTestCase):

    def test_add(self):
        # SET
        # RUN
        # ASSERT (EXP == ACT)
        assert utils.add(2, 2) == 4
        assert utils.add(0, 2) == 2
        assert utils.add(1, 2) == 3
        assert utils.add(-1, 2) == 1
        assert utils.add(2, 0) == 2
        assert utils.add(2, 1) == 3
        assert utils.add(2, -1) == 1

    def test_frange(self):
        # SET
        # RUN
        # ASSERT (EXP == ACT)
        self.assertEqual(list(utils.frange(5)), [0, 1, 2, 3, 4])
        self.assertEqual(list(utils.frange(2, 5)), [2, 3, 4])
        self.assertEqual(list(utils.frange(2, 10, 2)), [2, 4, 6, 8])
        self.assertEqual(list(utils.frange(10, 2, -2)), [10, 8, 6, 4])

        self.assertEqual(list(utils.frange(1, 5)), [1, 2, 3, 4])
        self.assertEqual(list(utils.frange(0, 5)), [0, 1, 2, 3, 4])
        self.assertEqual(list(utils.frange(0, 0)), [])
        self.assertEqual(list(utils.frange(100, 0)), [])
