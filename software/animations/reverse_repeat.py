def reverse(collection):
    l = list(collection)
    l.reverse()
    return l


class ReverseRepeatIterator(object):
    def __init__(self, collection):
        l = list(collection)
        self.cycle_length = len(l)
        self.collection = l + reverse(l)[1:] + l[1:] + reverse(l)[1:]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        clamped_index = self.index % (self.cycle_length * 2 - 2)
        result = self.collection[clamped_index:(clamped_index + self.cycle_length)]
        self.index += 1
        return result
