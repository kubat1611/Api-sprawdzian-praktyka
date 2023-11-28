import unittest
from src.tests.test_unit import TestAppUnit


def run_tests(test_class):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_class)

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests(TestAppUnit)

    if success:
        print("\n\033[92mAll tests passed.\033[0m")
    else:
        print("\n\033[91mSome tests failed.\033[0m")
