

class FilterXchar:
    """
    Filter seqs with non-protein character `X` percentage >= threshold
    """

    def __init__(self, th=5.0):
        self.th = th

    def apply(self, records):
        xf = lambda item: not (item.seq.count('X') / len(item.seq)) * 100 >= self.th
        return filter(xf, records)


class Filterlen:
    """
    Filter seqs with len < max seq len
    """

    def __init__(self, maxlen):
        self.maxlen = maxlen

    def apply(self, records):
        lf = lambda item: not (len(item.seq)) < self.maxlen
        return filter(lf, records)


class FilterCountry:
    """
    Filter by choosen country
    """

    def __init__(self, country):
        self.country = country

    def apply(self, records):
        lf = lambda item: item.description.split('|')[-1] == self.country
        return filter(lf, records)