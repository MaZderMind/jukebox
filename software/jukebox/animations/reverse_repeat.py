from animations.direction import Direction


def reverse(collection):
    l = list(collection)
    l.reverse()
    return l


class ReverseRepeatIterator(object):
    """
    From a Series of ABCD this Iterator returns repeating permutation of this sequence without jumps:
    ABCD, BCDC, CDCB, DCBA, CBAB, BABC, ABCD returning to the start
    given that A, B, C and D are colors, this gives a step-free color rotation
    """

    def __init__(self, collection, direction=Direction.FORWARD):
        l = list(collection)
        self.cycle_length = len(l)
        # Stores ABCD as ABCD_CBA_BCD of which a sliding window is iterated:
        self.collection = l + reverse(l)[1:] + l[1:]
        self.index = 0
        self.direction = direction

    def __iter__(self):
        return self

    def __next__(self):
        clamped_index = self.index % (self.cycle_length * 2 - 2)
        result = self.collection[clamped_index:(clamped_index + self.cycle_length)]
        self.index += -1 if self.direction == Direction.FORWARD else +1
        return result
