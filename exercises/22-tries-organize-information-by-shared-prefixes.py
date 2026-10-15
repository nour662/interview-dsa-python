"""Exercise 22: Tries: organize information by shared prefixes. See ../lessons/22-tries-organize-information-by-shared-prefixes.md.
Run from the repository root with: python -m unittest discover -s tests -v
Reference tests check solutions by default; use the exercise grader documented in README.
"""

class PrefixIndex:
    """Trie with duplicate inserts counted as separate entries."""

    def __init__(self):
        raise NotImplementedError()

    def add(self, word):
        raise NotImplementedError()

    def count_prefix(self, prefix):
        raise NotImplementedError()
