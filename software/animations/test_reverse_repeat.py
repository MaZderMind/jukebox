from unittest import TestCase

from reverse_repeat import ReverseRepeatIterator


class TestReverseRepeatIterator(TestCase):
    def testThreeItems(self):
        iterator = ReverseRepeatIterator(['A', 'B', 'C'])

        for _ in range(3):
            assert next(iterator) == ['A', 'B', 'C']

            assert next(iterator) == ['B', 'C', 'B']
            assert next(iterator) == ['C', 'B', 'A']
            assert next(iterator) == ['B', 'A', 'B']

            assert next(iterator) == ['A', 'B', 'C']
            assert next(iterator) == ['B', 'C', 'B']
            assert next(iterator) == ['C', 'B', 'A']
            assert next(iterator) == ['B', 'A', 'B']

    def testFiveItems(self):
        iterator = ReverseRepeatIterator(['A', 'B', 'C', 'D', 'E', 'F'])

        for _ in range(3):
            assert next(iterator) == ['A', 'B', 'C', 'D', 'E', 'F']

            assert next(iterator) == ['B', 'C', 'D', 'E', 'F', 'E']
            assert next(iterator) == ['C', 'D', 'E', 'F', 'E', 'D']
            assert next(iterator) == ['D', 'E', 'F', 'E', 'D', 'C']
            assert next(iterator) == ['E', 'F', 'E', 'D', 'C', 'B']

            assert next(iterator) == ['F', 'E', 'D', 'C', 'B', 'A']

            assert next(iterator) == ['E', 'D', 'C', 'B', 'A', 'B']
            assert next(iterator) == ['D', 'C', 'B', 'A', 'B', 'C']
            assert next(iterator) == ['C', 'B', 'A', 'B', 'C', 'D']
            assert next(iterator) == ['B', 'A', 'B', 'C', 'D', 'E']
