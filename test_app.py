import unittest

class TestApp(unittest.TestCase):
    def test_always_fail(self):
        self.assertEqual(1, 2, "Test échoue intentionnellement pour validation")

if __name__ == '__main__':
    unittest.main()