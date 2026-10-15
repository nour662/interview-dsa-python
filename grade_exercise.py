"""Run one lesson's tests against the learner's starter implementation."""
import argparse
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson', type=int, choices=range(1, 27))
    args = parser.parse_args()
    entry = json.loads((ROOT / 'course.json').read_text())[args.lesson - 1]
    spec = importlib.util.spec_from_file_location('learner_attempt', ROOT / entry['exercise'])
    attempt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(attempt)
    from solutions import core
    setattr(core, entry['symbol'], getattr(attempt, entry['symbol']))
    tests_spec = importlib.util.spec_from_file_location('reference_tests', ROOT / 'tests/test_course.py')
    tests_module = importlib.util.module_from_spec(tests_spec)
    tests_spec.loader.exec_module(tests_module)
    names = [name for name in unittest.defaultTestLoader.getTestCaseNames(tests_module.CourseTests)
             if name.startswith(f'test_{args.lesson:02d}_')]
    suite = unittest.TestSuite(tests_module.CourseTests(name) for name in names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
